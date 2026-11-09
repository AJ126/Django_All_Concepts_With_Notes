document.addEventListener("DOMContentLoaded", function () {
    var togglers = document.querySelectorAll("[data-nav-toggle='dropdown']");

    function closeDropdowns(except) {
        document.querySelectorAll(".navbar .dropdown-menu.show").forEach(function (menu) {
            if (menu !== except) {
                menu.classList.remove("show");
                var toggle = menu.parentElement.querySelector("[data-nav-toggle='dropdown']");
                if (toggle) {
                    toggle.setAttribute("aria-expanded", "false");
                }
            }
        });
    }

    document.querySelectorAll("[data-nav-toggle='collapse']").forEach(function (toggle) {
        toggle.addEventListener("click", function () {
            var target = document.querySelector(toggle.getAttribute("data-nav-target"));
            if (target) {
                var expanded = target.classList.toggle("show");
                toggle.setAttribute("aria-expanded", String(expanded));
            }
        });
    });

    togglers.forEach(function (toggle) {
        toggle.addEventListener("click", function (event) {
            event.preventDefault();
            var menu = toggle.parentElement.querySelector(".dropdown-menu");
            if (!menu) {
                return;
            }
            var opening = !menu.classList.contains("show");
            closeDropdowns(menu);
            menu.classList.toggle("show", opening);
            toggle.setAttribute("aria-expanded", String(opening));
        });
    });

    document.addEventListener("click", function (event) {
        if (!event.target.closest(".navbar .dropdown")) {
            closeDropdowns(null);
        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            closeDropdowns(null);
        }
    });
});
