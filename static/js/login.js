/* ─── login.js ───────────────────────────────────────────────── */

$(document).ready(function () {

    /* ── Tab switching ─────────────────────────────────────── */
    function showTab(tab) {
        if (tab === 'login') {
            $('#form-login').show();
            $('#form-signup').hide();
            $('#tab-login').addClass('active');
            $('#tab-signup').removeClass('active');
            $('#auth-heading').text('Welcome back');
            $('#auth-subheading').text('Log in to access your reviews and profile.');
        } else {
            $('#form-login').hide();
            $('#form-signup').show();
            $('#tab-login').removeClass('active');
            $('#tab-signup').addClass('active');
            $('#auth-heading').text('Create an account');
            $('#auth-subheading').text('Join UWA students sharing honest unit reviews.');
        }
    }

    $('#tab-login').on('click', function () { showTab('login'); });
    $('#tab-signup').on('click', function () { showTab('signup'); });

    /* ── Password strength indicator ──────────────────────── */
    $('#signup-password').on('input', function () {
        var val   = $(this).val();
        var bars  = $('.pw-bar');
        var label = $('#pw-label');

        bars.removeClass('weak fair strong');

        if (val.length === 0) {
            label.text('');
            return;
        }

        var strength = 0;
        if (val.length >= 8) strength++;
        if (/[A-Z]/.test(val) && /[a-z]/.test(val)) strength++;
        if (/[0-9]/.test(val) || /[^A-Za-z0-9]/.test(val)) strength++;

        if (strength === 1) {
            bars.eq(0).addClass('weak');
            label.text('Weak').css('color', '#A32D2D');
        } else if (strength === 2) {
            bars.eq(0).add(bars.eq(1)).addClass('fair');
            label.text('Fair').css('color', '#BA7517');
        } else {
            bars.addClass('strong');
            label.text('Strong').css('color', '#1D9E75');
        }
    });

    /* ── Confirm password match indicator ─────────────────── */
    $('#signup-confirm').on('input', function () {
        var pw      = $('#signup-password').val();
        var confirm = $(this).val();
        if (confirm.length === 0) {
            $(this).removeClass('is-invalid is-valid');
            return;
        }
        if (pw === confirm) {
            $(this).removeClass('is-invalid').addClass('is-valid');
        } else {
            $(this).removeClass('is-valid').addClass('is-invalid');
        }
    });

    /* ── Clear validation state on input ──────────────────── */
    $('.form-control').on('input', function () {
        $(this).removeClass('is-invalid');
    });

});
