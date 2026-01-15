// ========================================
// PORTFOLIO WEBSITE - JAVASCRIPT
// ======================================== 

// ========================================
// THEME MANAGEMENT
// ========================================

class ThemeManager {
  constructor() {
    // Default to light theme
    this.theme = localStorage.getItem('theme') || 'light';
    this.toggleBtn = document.getElementById('themeToggle');
    this.init();
  }

  init() {
    this.applyTheme();
    this.setupEventListeners();
  }

  setupEventListeners() {
    if (this.toggleBtn) {
      this.toggleBtn.addEventListener('click', () => this.toggle());
    }
  }

  applyTheme() {
    document.documentElement.setAttribute('data-theme', this.theme);
    if (this.toggleBtn) {
      const icon = this.toggleBtn.querySelector('i');
      if (icon) {
        // Show moon icon in light mode (to switch to dark), sun icon in dark mode (to switch to light)
        icon.className = this.theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
      }
    }
  }

  toggle() {
    this.theme = this.theme === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', this.theme);
    this.applyTheme();
  }
}

// ========================================
// NAVIGATION MANAGEMENT
// ========================================

class NavManager {
  constructor() {
    this.hamburger = document.getElementById('hamburger');
    this.navMenu = document.getElementById('navMenu');
    this.navLinks = document.querySelectorAll('.nav-link');
    this.init();
  }

  init() {
    if (this.hamburger) {
      this.hamburger.addEventListener('click', () => this.toggleMenu());
    }

    this.navLinks.forEach(link => {
      link.addEventListener('click', () => {
        this.closeMenu();
        this.updateActiveLink();
      });
    });

    window.addEventListener('scroll', () => this.updateActiveLink());
  }

  toggleMenu() {
    this.hamburger.classList.toggle('active');
    this.navMenu.classList.toggle('active');
  }

  closeMenu() {
    this.hamburger.classList.remove('active');
    this.navMenu.classList.remove('active');
  }

  updateActiveLink() {
    const sections = document.querySelectorAll('section');
    let current = '';

    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.clientHeight;
      if (scrollY >= sectionTop - 200) {
        current = section.getAttribute('id');
      }
    });

    this.navLinks.forEach(link => {
      link.classList.remove('active');
      const href = link.getAttribute('href');
      if (current && href.includes(current)) {
        link.classList.add('active');
      }
    });
  }
}

// ========================================
// SCROLL ANIMATIONS
// ========================================

class ScrollAnimations {
  constructor() {
    this.init();
  }

  init() {
    const options = {
      threshold: 0.1,
      rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.animation = 'fadeIn 0.6s ease-out forwards';
          observer.unobserve(entry.target);
        }
      });
    }, options);

    document.querySelectorAll('.skill-item, .project-card, .timeline-item, .contact-item').forEach(el => {
      el.style.opacity = '0';
      observer.observe(el);
    });
  }
}

// ========================================
// FORM HANDLING
// ========================================

class FormHandler {
  constructor() {
    this.form = document.querySelector('.contact-form form');
    this.init();
  }

  init() {
    if (this.form) {
      this.form.addEventListener('submit', (e) => this.handleSubmit(e));
      this.setupValidation();
    }
  }

  setupValidation() {
    const inputs = this.form.querySelectorAll('input[type="text"], input[type="email"], textarea');
    inputs.forEach(input => {
      input.addEventListener('blur', () => this.validateField(input));
      input.addEventListener('focus', () => this.clearError(input));
    });
  }

  validateField(field) {
    const value = field.value.trim();
    const fieldType = field.type;

    let isValid = value.length > 0;

    if (fieldType === 'email') {
      isValid = this.isValidEmail(value);
    }

    if (!isValid) {
      field.style.borderColor = '#ff6b6b';
      field.style.boxShadow = '0 0 0 3px rgba(255, 107, 107, 0.15)';
    }
  }

  clearError(field) {
    field.style.borderColor = '';
    field.style.boxShadow = '';
  }

  isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  }

  handleSubmit(e) {
    // Let Django handle the form submission
    // This is just for client-side feedback
  }
}

// ========================================
// SKILL ANIMATION
// ========================================

class SkillAnimation {
  constructor() {
    this.skillItems = document.querySelectorAll('.skill-item');
    this.init();
  }

  init() {
    const options = {
      threshold: 0.5,
      rootMargin: '0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.animateSkill(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, options);

    this.skillItems.forEach(item => {
      observer.observe(item);
    });
  }

  animateSkill(item) {
    const icon = item.querySelector('i');
    if (icon) {
      icon.style.animation = 'float 0.6s ease-out forwards';
    }
  }
}

// ========================================
// CODE HIGHLIGHTING
// ========================================

class CodeHighlight {
  constructor() {
    this.init();
  }

  init() {
    if (typeof hljs !== 'undefined') {
      document.querySelectorAll('pre code').forEach(block => {
        hljs.highlightElement(block);
      });
    }
  }
}

// ========================================
// SMOOTH SCROLL
// ========================================

class SmoothScroll {
  constructor() {
    this.init();
  }

  init() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', (e) => {
        const href = anchor.getAttribute('href');
        if (href !== '#') {
          e.preventDefault();
          const target = document.querySelector(href);
          if (target) {
            target.scrollIntoView({
              behavior: 'smooth',
              block: 'start'
            });
          }
        }
      });
    });
  }
}

// ========================================
// UTILITY FUNCTIONS
// ========================================

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// ========================================
// INITIALIZATION
// ========================================

document.addEventListener('DOMContentLoaded', () => {
  // Initialize all components
  new ThemeManager();
  new NavManager();
  new ScrollAnimations();
  new FormHandler();
  new SkillAnimation();
  new CodeHighlight();
  new SmoothScroll();

  console.log('✨ Portfolio initialized successfully!');
});

// ========================================
// HANDLE RESPONSIVE ADJUSTMENTS
// ========================================

const handleResize = debounce(() => {
  // Recalculate any responsive values if needed
}, 250);

window.addEventListener('resize', handleResize);

// ========================================
// ACCESSIBILITY ENHANCEMENTS
// ========================================

// Add keyboard navigation support
document.addEventListener('keydown', (e) => {
  // ESC to close mobile menu
  if (e.key === 'Escape') {
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('navMenu');
    if (hamburger && navMenu) {
      hamburger.classList.remove('active');
      navMenu.classList.remove('active');
    }
  }
});

// ========================================
// PERFORMANCE OPTIMIZATION
// ========================================

// Lazy load images if supported
if ('IntersectionObserver' in window) {
  const images = document.querySelectorAll('img[data-src]');
  const imageObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
        imageObserver.unobserve(img);
      }
    });
  });

  images.forEach(img => imageObserver.observe(img));
}