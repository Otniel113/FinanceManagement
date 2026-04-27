document.addEventListener("DOMContentLoaded", () => {
  const yearTargets = document.querySelectorAll(
    "#current-year, [data-current-year]",
  );
  yearTargets.forEach((target) => {
    target.textContent = new Date().getFullYear();
  });

  const internalLinks = document.querySelectorAll('a[href^="#"]');

  internalLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
      const targetId = link.getAttribute("href");

      if (!targetId || targetId === "#") return;

      const targetElement = document.querySelector(targetId);

      if (!targetElement) return;

      event.preventDefault();

      targetElement.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    });
  });

  const navLinks = document.querySelectorAll(
    ".navbar-nav .nav-link[href^='#']",
  );
  const sections = Array.from(navLinks)
    .map((link) => document.querySelector(link.getAttribute("href")))
    .filter(Boolean);

  const setActiveLink = (sectionId) => {
    navLinks.forEach((link) => {
      const isActive = link.getAttribute("href") === `#${sectionId}`;
      link.classList.toggle("active", isActive);
      link.setAttribute("aria-current", isActive ? "page" : "false");
    });
  };

  if ("IntersectionObserver" in window && sections.length > 0) {
    const observer = new IntersectionObserver(
      (entries) => {
        const visibleEntry = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

        if (visibleEntry) {
          setActiveLink(visibleEntry.target.id);
        }
      },
      {
        root: null,
        threshold: [0.25, 0.4, 0.6],
        rootMargin: "-90px 0px -45% 0px",
      },
    );

    sections.forEach((section) => observer.observe(section));
  }

  const scrollTopButton = document.querySelector("[data-scroll-top]");

  if (scrollTopButton) {
    const toggleScrollTopButton = () => {
      scrollTopButton.classList.toggle("show", window.scrollY > 400);
    };

    scrollTopButton.addEventListener("click", () => {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    });

    window.addEventListener("scroll", toggleScrollTopButton, { passive: true });
    toggleScrollTopButton();
  }
});
