/* ─── unit.js ────────────────────────────────────────────────── */

$(document).ready(function () {

    /* ── Toggle review form (delegated handler) ────────────── */
    $(document).on('click', '.js-toggle-review-form', function (e) {
        e.preventDefault();
        $('#review-form').slideToggle(200);
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