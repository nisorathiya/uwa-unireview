/* ─── main.js — shared across all pages ──────────────────────── */

$(document).ready(function () {

    /* Auto-dismiss flash messages after 4 seconds */
    setTimeout(function () {
        $('.ur-flash').fadeOut(400);
    }, 4000);

});
