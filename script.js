document.addEventListener('DOMContentLoaded', () => {
  // --- Skills Section Progression Animation on Scroll ---
  const skillSection = document.querySelector('.skills-container');
  const progressBars = document.querySelectorAll('.skill-progress');

  const showProgress = () => {
    progressBars.forEach(bar => {
      const value = bar.getAttribute('data-value');
      bar.style.width = `${value}%`;
    });
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        showProgress();
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3 });

  if (skillSection) {
    observer.observe(skillSection);
  }

  // --- Active Nav Link highlighting on scroll ---
  const sections = document.querySelectorAll('section');
  const navLinks = document.querySelectorAll('.nav-links a');

  window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.clientHeight;
      if (pageYOffset >= (sectionTop - 150)) {
        current = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href').slice(1) === current) {
        link.classList.add('active');
      }
    });
  });

  // --- Interactive Typing Animation for Hero ---
  const typeText = document.querySelector('.typing-text');
  if (typeText) {
    const titles = ['Customer Science Analyst', 'Data Analyst', 'Economics Graduate'];
    let titleIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let delay = 200;

    const type = () => {
      const currentTitle = titles[titleIndex];
      if (isDeleting) {
        typeText.textContent = currentTitle.substring(0, charIndex - 1);
        charIndex--;
        delay = 100;
      } else {
        typeText.textContent = currentTitle.substring(0, charIndex + 1);
        charIndex++;
        delay = 200;
      }

      if (!isDeleting && charIndex === currentTitle.length) {
        isDeleting = true;
        delay = 2000; // Pause at end
      } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        titleIndex = (titleIndex + 1) % titles.length;
        delay = 500;
      }

      setTimeout(type, delay);
    };

    setTimeout(type, delay);
  }

  // --- Contact Form Submission Handling ---
  const form = document.querySelector('.contact-form');
  const toast = document.querySelector('.toast');

  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      
      // Simulate submission success
      toast.classList.add('show');
      form.reset();

      setTimeout(() => {
        toast.classList.remove('show');
      }, 4000);
    });
  }

  // --- Mobile Menu Toggle ---
  const menuToggle = document.querySelector('.menu-toggle');
  const navLinksList = document.querySelector('.nav-links');

  if (menuToggle && navLinksList) {
    menuToggle.addEventListener('click', () => {
      navLinksList.classList.toggle('open');
    });

    // Close mobile menu when a link is clicked
    navLinksList.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinksList.classList.remove('open');
      });
    });
  }
});
