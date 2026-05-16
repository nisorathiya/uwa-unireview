/**
 * Reusable toast/flash notification system.
 *
 * Exposes a single global function window.showFlash(message, category)
 * used by:
 *   - Server-side flash() calls (rendered from base.html on page load)
 *   - Client-side JS (AJAX failures, form-validation feedback, etc.)
 *
 * Categories: 'info', 'success', 'warning', 'danger' (alias: 'error').
 */
(function () {
  'use strict';

  // Lazily create the container on first use, then reuse it.
  function getContainer() {
    var container = document.getElementById('ur-toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'ur-toast-container';
      container.className = 'ur-toast-container';
      // Accessibility: screen readers announce new toasts as they appear.
      container.setAttribute('role', 'region');
      container.setAttribute('aria-live', 'polite');
      container.setAttribute('aria-label', 'Notifications');
      document.body.appendChild(container);
    }
    return container;
  }

  /**
   * Show a toast notification.
   * @param {string} message  - The text to display.
   * @param {string} category - One of: info, success, warning, danger/error.
   * @param {number} [duration=4000] - Auto-dismiss after N ms. 0 = persist.
   */
  window.showFlash = function (message, category, duration) {
    category = category || 'info';
    duration = (typeof duration === 'number') ? duration : 4000;

    var container = getContainer();

    var toast = document.createElement('div');
    toast.className = 'ur-toast ur-toast-' + category;
    toast.setAttribute('role', category === 'danger' || category === 'error'
                               ? 'alert' : 'status');

    var msg = document.createElement('span');
    msg.className = 'ur-toast-message';
    msg.textContent = message;   // textContent, not innerHTML — prevents XSS

    var close = document.createElement('button');
    close.className = 'ur-toast-close';
    close.setAttribute('aria-label', 'Dismiss notification');
    close.innerHTML = '&times;';
    close.onclick = function () { dismiss(toast); };

    toast.appendChild(msg);
    toast.appendChild(close);
    container.appendChild(toast);

    // Trigger the slide-in transition on next frame.
    requestAnimationFrame(function () {
      toast.classList.add('ur-toast-show');
    });

    if (duration > 0) {
      setTimeout(function () { dismiss(toast); }, duration);
    }

    return toast;
  };

  function dismiss(toast) {
    if (!toast || !toast.parentNode) return;
    toast.classList.remove('ur-toast-show');
    // Wait for the CSS transition to finish before removing from DOM.
    setTimeout(function () {
      if (toast.parentNode) toast.parentNode.removeChild(toast);
    }, 200);
  }

  /**
   * Show a confirmation modal. Returns a Promise that resolves to
   * true (confirmed) or false (cancelled).
   * Used by the delete-review flow.
   */
  window.showConfirm = function (opts) {
    opts = opts || {};
    var title       = opts.title       || 'Are you sure?';
    var body        = opts.body        || '';
    var confirmText = opts.confirmText || 'Confirm';
    var cancelText  = opts.cancelText  || 'Cancel';
    var danger      = !!opts.danger;

    return new Promise(function (resolve) {
      var backdrop = document.createElement('div');
      backdrop.className = 'ur-modal-backdrop';
      backdrop.innerHTML =
        '<div class="ur-modal" role="dialog" aria-modal="true">' +
          '<div class="ur-modal-title"></div>' +
          '<div class="ur-modal-body"></div>' +
          '<div class="ur-modal-actions">' +
            '<button type="button" class="ur-btn ur-btn-ghost ur-modal-cancel"></button>' +
            '<button type="button" class="ur-btn ur-modal-confirm"></button>' +
          '</div>' +
        '</div>';
      document.body.appendChild(backdrop);

      // textContent, not innerHTML — caller-supplied strings are not trusted.
      backdrop.querySelector('.ur-modal-title').textContent  = title;
      backdrop.querySelector('.ur-modal-body').textContent   = body;
      backdrop.querySelector('.ur-modal-cancel').textContent = cancelText;
      var confirmBtn = backdrop.querySelector('.ur-modal-confirm');
      confirmBtn.textContent = confirmText;
      confirmBtn.classList.add(danger ? 'ur-btn-danger' : 'ur-btn-primary');

      function close(result) {
        backdrop.classList.remove('ur-modal-show');
        setTimeout(function () {
          if (backdrop.parentNode) backdrop.parentNode.removeChild(backdrop);
        }, 200);
        resolve(result);
      }

      backdrop.querySelector('.ur-modal-cancel').onclick  = function () { close(false); };
      confirmBtn.onclick                                  = function () { close(true);  };
      backdrop.onclick = function (e) { if (e.target === backdrop) close(false); };

      requestAnimationFrame(function () {
        backdrop.classList.add('ur-modal-show');
      });
    });
  };
})();