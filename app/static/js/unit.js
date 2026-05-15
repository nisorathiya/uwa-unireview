/* ─── unit.js ────────────────────────────────────────────────── */
$(document).ready(function () {
    /* Validate review form before submission — replaces HTML5
       required/minlength so we can show our own toast instead of
       the native browser popup. */
    $(document).on('submit', '#review-form form', function (e) {
        var $comment = $(this).find('textarea[name="comment"]');
        var value = ($comment.val() || '').trim();

        if (value.length < 20) {
            e.preventDefault();
            window.showFlash(
                'Please write at least 20 characters in your review.',
                'warning'
            );
            $comment.focus();
            return false;
        }
    });

    /* Confirm delete review via styled modal — replaces the
       native browser confirm() dialog. */
    $(document).on('submit', '.js-delete-review-form', function (e) {
        var $form = $(this);

        // If the form is already flagged as confirmed, let it submit normally.
        if ($form.data('confirmed')) {
            return true;
        }

        e.preventDefault();

        window.showConfirm({
            title:       'Delete review?',
            body:        'This will permanently remove your review. This action cannot be undone.',
            confirmText: 'Delete',
            cancelText:  'Cancel',
            danger:      true,
        }).then(function (confirmed) {
            if (confirmed) {
                $form.data('confirmed', true);
                $form.trigger('submit');
            }
        });
    });

    /* Toggle review form */
    $(document).on('click', '.js-toggle-review-form', function (e) {
        e.preventDefault();
        // Reset form to submit (not edit) mode
        var $form = $('#review-form form');
        $form.attr('action', $form.data('submit-url'));
        $('#review-form-title').text('Your review');
        $('#review-form').slideToggle(200);
    });

    /* Edit review button */
    $(document).on('click', '.js-edit-review', function () {
        var reviewId = $(this).data('review-id');
        var $card = $('#review-' + reviewId);

        // Read existing values from the review card
        var overall = parseInt($card.find('.review-score-badge').text().match(/\d+/)[0]);
        var miniStats = $card.find('.review-mini-stat strong');
        var workload = parseInt($(miniStats[0]).text());
        var difficulty = parseInt($(miniStats[1]).text());
        var usefulness = parseInt($(miniStats[2]).text());
        var comment = $card.find('.review-comment').text().trim();

        // Pre-fill the form
        $('#slider-overall').val(overall); $('#val-overall').text(overall);
        $('#slider-workload').val(workload); $('#val-workload').text(workload);
        $('#slider-difficulty').val(difficulty); $('#val-difficulty').text(difficulty);
        $('#slider-usefulness').val(usefulness); $('#val-usefulness').text(usefulness);
        $('textarea[name="comment"]').val(comment);

        // Change form action to edit endpoint
        $('#review-form form').attr('action', '/review/edit/' + reviewId);
        $('#review-form-title').text('Edit your review');
        $('#review-form').slideDown(200);
        $('#review-form')[0].scrollIntoView({ behavior: 'smooth', block: 'start' });
    });

    /* ── Vote buttons (upvote / downvote) ──────────────────── */
    $(document).on('click', '.js-vote', function () {
        var $btn = $(this);
        var reviewId = $btn.data('review-id');
        var value = parseInt($btn.data('value'));
        var isActive = $btn.attr('data-active') === 'true';
        var sendValue = isActive ? 0 : value;

        $.ajax({
            url: '/api/vote',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ review_id: reviewId, value: sendValue }),
            headers: { 'X-CSRFToken': $('meta[name=csrf-token]').attr('content') },
            success: function (data) {
                var $row = $btn.closest('.review-vote-row');
                $row.find('.js-vote[data-value="1"] .vote-count').text(data.upvotes);
                $row.find('.js-vote[data-value="-1"] .vote-count').text(data.downvotes);
                $row.find('.js-vote').attr('data-active', 'false');
                if (sendValue !== 0) {
                    $btn.attr('data-active', 'true');
                }
            },
            error: function () {
                window.showFlash('Could not register vote. Please try again.', 'danger');
            }
        });
    });

    /* ── Save unit button ──────────────────────────────────── */
    $(document).on('click', '.js-save-btn', function () {
        var $btn = $(this);
        var unitId = $btn.data('unit-id');

        $.ajax({
            url: '/api/save-unit',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ unit_id: unitId }),
            headers: { 'X-CSRFToken': $('meta[name=csrf-token]').attr('content') },
            success: function (data) {
                if (data.saved) {
                    $btn.html('<i class="fa-solid fa-bookmark"></i> Saved');
                    $btn.removeClass('ur-btn-outline').addClass('ur-btn-saved');
                    window.showFlash('Unit saved to your bookmarks.', 'success');
                } else {
                    $btn.html('<i class="fa-regular fa-bookmark"></i> Save unit');
                    $btn.removeClass('ur-btn-saved').addClass('ur-btn-outline');
                    window.showFlash('Unit removed from your bookmarks.', 'info');
                }
            },
            error: function () {
                window.showFlash('Could not save unit. Please try again.', 'danger');
            }
        });
    });
    /* ── Rating distribution chart ─────────────────────────── */
    var $canvas = $('#rating-dist-chart');
    if ($canvas.length) {
        var dist = JSON.parse($canvas.attr('data-dist'));
        new Chart($canvas[0], {
            type: 'bar',
            data: {
                labels: ['1★', '2★', '3★', '4★', '5★'],
                datasets: [{
                    data: dist,
                    backgroundColor: 'rgba(37, 99, 235, 0.15)',
                    borderColor: 'rgba(37, 99, 235, 1)',
                    borderWidth: 1.5,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function (ctx) {
                                return ctx.parsed.y + ' review' + (ctx.parsed.y !== 1 ? 's' : '');
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 1, precision: 0 },
                        grid: { color: 'rgba(0,0,0,0.05)' }
                    },
                    x: { grid: { display: false } }
                }
            }
        });
    }
});