/* ─── dashboard.js ───────────────────────────────────────────── */

$(document).ready(function () {

    var activeFilter = 'all';
    var searchTimer  = null;

    /* ── Score pill helper ─────────────────────────────────── */
    function scorePill(val) {
        var cls = val >= 4.2 ? 'score-high' : val >= 3.5 ? 'score-mid' : 'score-low';
        return '<span class="score-pill ' + cls + '">&#9733; ' + val.toFixed(1) + '</span>';
    }

    /* ── Workload pill helper ──────────────────────────────── */
    function workloadPill(val) {
        var cls   = val >= 3.8 ? 'score-high' : val >= 3.0 ? 'score-mid' : 'score-low';
        var label = val >= 3.8 ? 'Light load'  : val >= 3.0 ? 'Moderate'   : 'Heavy load';
        return '<span class="score-pill ' + cls + '">' + label + '</span>';
    }

    /* ── Render unit cards ─────────────────────────────────── */
    function renderUnits(units) {
        var $grid = $('#unit-grid');
        $grid.empty();

        $('#unit-count').text(units.length + ' units');

        if (units.length === 0) {
            $grid.html(
                '<div class="ur-empty">' +
                '<i class="fa-solid fa-magnifying-glass"></i>' +
                '<p>No units match your search. Try a different keyword or filter.</p>' +
                '</div>'
            );
            return;
        }

        $.each(units, function (i, u) {
            var facultyLabel = u.faculty.charAt(0).toUpperCase() + u.faculty.slice(1);
            var card =
                '<a href="/unit/' + u.id + '" class="ur-unit-card">' +
                  '<div class="ur-unit-code">' + u.code + '</div>' +
                  '<div class="ur-unit-name">'  + u.name + '</div>' +
                  '<div class="ur-unit-faculty">' + facultyLabel + '</div>' +
                  '<div class="ur-unit-scores">' +
                    scorePill(u.overall) +
                    workloadPill(u.workload) +
                  '</div>' +
                  '<div class="ur-unit-footer">' +
                    '<span class="ur-unit-reviews">' + u.reviews + ' reviews</span>' +
                    '<span class="ur-unit-arrow">&#8594;</span>' +
                  '</div>' +
                '</a>';
            $grid.append(card);
        });
    }

    /* ── AJAX search — calls Flask /api/search ─────────────── */
    function fetchUnits() {
        var q = $('#search-input').val();

        $.ajax({
            url: '/api/search',
            method: 'GET',
            data: { q: q, faculty: activeFilter },
            success: function (data) {
                renderUnits(data);
            },
            error: function () {
                $('#unit-grid').html(
                    '<div class="ur-empty">' +
                    '<p>Could not load units. Please refresh the page.</p>' +
                    '</div>'
                );
            }
        });
    }

    /* ── Search input (debounced 220ms) ────────────────────── */
    $('#search-input').on('input', function () {
        clearTimeout(searchTimer);
        searchTimer = setTimeout(fetchUnits, 220);
    });

    /* ── Faculty filter pills ──────────────────────────────── */
    $('.ur-filter-pill').on('click', function () {
        $('.ur-filter-pill').removeClass('active');
        $(this).addClass('active');
        activeFilter = $(this).data('faculty');
        fetchUnits();
    });

    /* ── Initial load ──────────────────────────────────────── */
    fetchUnits();

});
