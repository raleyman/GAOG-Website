// Mobile nav toggle
document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.querySelector(".nav-toggle");
  var links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var isOpen = links.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
    links.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        links.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // Transparent header over the hero, solidifying once scrolled past it
  var header = document.querySelector(".site-header");
  var hero = document.querySelector(".hero");
  if (header && hero) {
    document.body.classList.add("has-hero");
    var updateHeader = function () {
      var threshold = Math.max(hero.offsetHeight - header.offsetHeight, 40);
      if (window.scrollY > threshold) {
        header.classList.add("is-scrolled");
      } else {
        header.classList.remove("is-scrolled");
      }
    };
    updateHeader();
    window.addEventListener("scroll", updateHeader, { passive: true });
    window.addEventListener("resize", updateHeader);
  }

  // Mark current nav link active
  var path = window.location.pathname.replace(/\/index\.html$/, "/").replace(/\.html$/, "");
  if (path === "" ) path = "/";
  document.querySelectorAll(".nav-links a[data-path]").forEach(function (a) {
    if (a.getAttribute("data-path") === path) {
      a.classList.add("is-active");
    }
  });

  // Team biography modal (click a photo / "Read Full Biography" to open)
  var overlay = document.getElementById("bioModalOverlay");
  if (overlay) {
    var modalAvatar = document.getElementById("bioModalAvatar");
    var modalName = document.getElementById("bioModalName");
    var modalRole = document.getElementById("bioModalRole");
    var modalBody = document.getElementById("bioModalBody");
    var modalEdu = document.getElementById("bioModalEdu");
    var closeBtn = document.getElementById("bioModalClose");
    var lastFocused = null;

    function getFocusableInModal() {
      var selector = 'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])';
      return Array.prototype.filter.call(
        overlay.querySelectorAll(selector),
        function (el) { return el.offsetParent !== null; }
      );
    }

    function trapFocus(e) {
      if (e.key !== "Tab" || overlay.hidden) return;
      var focusable = getFocusableInModal();
      if (!focusable.length) return;
      var first = focusable[0];
      var last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }

    function openBio(id) {
      var tpl = document.getElementById(id);
      if (!tpl) return;
      lastFocused = document.activeElement;
      var photo = tpl.getAttribute("data-photo") || "";
      if (photo) {
        modalAvatar.innerHTML = '<img src="' + photo + '" alt="" />';
      } else {
        modalAvatar.textContent = tpl.getAttribute("data-initials") || "";
      }
      modalName.textContent = tpl.getAttribute("data-name") || "";
      modalRole.textContent = tpl.getAttribute("data-role") || "";
      modalBody.innerHTML = tpl.innerHTML;
      var edu = tpl.getAttribute("data-edu") || "";
      modalEdu.textContent = edu;
      modalEdu.style.display = edu ? "" : "none";
      overlay.hidden = false;
      document.body.style.overflow = "hidden";
      closeBtn.focus();
    }

    function closeBio() {
      overlay.hidden = true;
      document.body.style.overflow = "";
      if (lastFocused && lastFocused.focus) lastFocused.focus();
    }

    document.querySelectorAll("[data-bio-open]").forEach(function (el) {
      el.addEventListener("click", function () {
        openBio(el.getAttribute("data-bio-open"));
      });
      el.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          openBio(el.getAttribute("data-bio-open"));
        }
      });
    });

    closeBtn.addEventListener("click", closeBio);
    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) closeBio();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !overlay.hidden) closeBio();
      trapFocus(e);
    });
  }
});
