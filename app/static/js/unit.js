/* ─── unit.js ────────────────────────────────────────────────── */

$(document).ready(function () {

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
        var $card    = $('#review-' + reviewId);

        // Read existing values from the review card
        var overall    = parseInt($card.find('.review-score-badge').text().match(/\d+/)[0]);
        var miniStats  = $card.find('.review-mini-stat strong');
        var workload   = parseInt($(miniStats[0]).text());
        var difficulty = parseInt($(miniStats[1]).text());
        var usefulness = parseInt($(miniStats[2]).text());
        var comment    = $card.find('.review-comment').text().trim();

        // Pre-fill the form
        $('#slider-overall').val(overall);    $('#val-overall').text(overall);
        $('#slider-workload').val(workload);   $('#val-workload').text(workload);
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
        var $btn      = $(this);
        var reviewId  = $btn.data('review-id');
        var value     = parseInt($btn.data('value'));
        var isActive  = $btn.attr('data-active') === 'true';
        var sendValue = isActive ? 0 : value;

        $.ajax({
            url:    '/api/vote',
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
                alert('Could not register vote. Please try again.');
            }
        });
    });

    /* ── Save unit button ──────────────────────────────────── */
    $(document).on('click', '.js-save-btn', function () {
        var $btn   = $(this);
        var unitId = $btn.data('unit-id');

        $.ajax({
            url:    '/api/save-unit',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ unit_id: unitId }),
            headers: { 'X-CSRFToken': $('meta[name=csrf-token]').attr('content') },
            success: function (data) {
                if (data.saved) {
                    $btn.html('<i class="fa-solid fa-bookmark"></i> Saved');
                    $btn.removeClass('ur-btn-outline').addClass('ur-btn-saved');
                } else {
                    $btn.html('<i class="fa-regular fa-bookmark"></i> Save unit');
                    $btn.removeClass('ur-btn-saved').addClass('ur-btn-outline');
                }
            },
            error: function () {
                alert('Could not save unit. Please try again.');
            }
        });
    });

});