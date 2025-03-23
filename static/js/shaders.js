// Modern UI color system and theme management
class ThemeManager {
  constructor() {
    this.darkMode = localStorage.getItem('darkMode') === 'true';
    this.initThemeToggle();
    this.applyTheme();
    this.generateDynamicColors();
    this.setupChartThemes();
  }
  
  // Initialize theme toggle button
  initThemeToggle() {
    const themeBtn = document.getElementById('themeToggleBtn');
    if (themeBtn) {
      themeBtn.innerHTML = this.darkMode ? '<i class="bi bi-sun"></i>' : '<i class="bi bi-moon"></i>';
      themeBtn.addEventListener('click', () => this.toggleTheme());
    }
  }
  
  // Toggle between light and dark themes
  toggleTheme() {
    this.darkMode = !this.darkMode;
    localStorage.setItem('darkMode', this.darkMode);
    
    const themeBtn = document.getElementById('themeToggleBtn');
    if (themeBtn) {
      themeBtn.innerHTML = this.darkMode ? '<i class="bi bi-sun"></i>' : '<i class="bi bi-moon"></i>';
    }
    
    this.applyTheme();
    this.updateChartThemes();
  }
  
  // Apply the selected theme to the UI
  applyTheme() {
    document.body.classList.toggle('dark-mode', this.darkMode);
    
    // Update meta theme-color for mobile browsers
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
      metaThemeColor.setAttribute('content', this.darkMode ? '#121212' : '#f8f9fa');
    }
  }
  
  // Generate dynamic color variations
  generateDynamicColors() {
    const primaryColor = getComputedStyle(document.documentElement).getPropertyValue('--primary').trim();
    const rgb = this.hexToRgb(primaryColor || '#4361ee');
    
    if (!rgb) return;
    
    const root = document.documentElement;
    
    // Generate complementary and analogous colors
    const complementary = this.calculateComplementary(rgb);
    root.style.setProperty('--complementary', this.rgbToHex(complementary));
    
    // Add support for light background variations
    root.style.setProperty('--primary-light-bg', `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, 0.1)`);
    root.style.setProperty('--primary-lighter-bg', `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, 0.05)`);
  }
  
  // Set up Chart.js theme defaults
  setupChartThemes() {
    if (typeof Chart !== 'undefined') {
      Chart.defaults.font.family = getComputedStyle(document.documentElement).getPropertyValue('--font-family').trim();
      Chart.defaults.font.size = 12;
      Chart.defaults.plugins.legend.labels.usePointStyle = true;
      Chart.defaults.plugins.tooltip.cornerRadius = 8;
      Chart.defaults.plugins.tooltip.padding = 12;
      Chart.defaults.elements.point.radius = 4;
      
      this.updateChartThemes();
    }
  }
  
  // Update Chart.js themes based on current mode
  updateChartThemes() {
    if (typeof Chart === 'undefined') return;
    
    if (this.darkMode) {
      Chart.defaults.color = '#adb5bd';
      Chart.defaults.borderColor = '#333';
      Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(40, 44, 52, 0.9)';
      Chart.defaults.plugins.tooltip.titleColor = '#f8f9fa';
      Chart.defaults.plugins.tooltip.bodyColor = '#f8f9fa';
    } else {
      Chart.defaults.color = '#666';
      Chart.defaults.borderColor = '#e9ecef';
      Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(255, 255, 255, 0.95)';
      Chart.defaults.plugins.tooltip.titleColor = '#333';
      Chart.defaults.plugins.tooltip.bodyColor = '#333';
    }
    
    // Refresh any charts on the page if they exist
    try {
      if (window.statusChart && typeof window.statusChart.update === 'function') {
        window.statusChart.update();
      }
      if (window.priorityChart && typeof window.priorityChart.update === 'function') {
        window.priorityChart.update();
      }
    } catch (e) {
      console.log("Charts not available on this page");
    }
  }
  
  // Color utility functions
  hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    } : null;
  }
  
  rgbToHex({r, g, b}) {
    return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1)}`;
  }
  
  calculateComplementary({r, g, b}) {
    return {r: 255 - r, g: 255 - g, b: 255 - b};
  }
}

// UI enhancements for modern interactions
class UIEnhancer {
  constructor() {
    this.initializeAnimations();
    this.setupAccessibility();
    this.enhanceFormExperience();
    this.addMobileOptimizations();
  }
  
  // Initialize animations and transitions
  initializeAnimations() {
    // Add fade-in animation to cards
    document.querySelectorAll('.card, .stat-card').forEach((element, index) => {
      element.style.animationDelay = `${index * 0.05}s`;
      element.classList.add('fade-in');
    });
    
    // Enhance hover effects
    document.querySelectorAll('.card, .btn, .badge').forEach(element => {
      element.addEventListener('mouseenter', () => {
        element.style.transition = 'all 0.2s ease-out';
      });
    });
  }
  
  // Improve accessibility features
  setupAccessibility() {
    // Add aria attributes where missing
    document.querySelectorAll('button:not([aria-label])').forEach(button => {
      if (button.textContent.trim()) {
        button.setAttribute('aria-label', button.textContent.trim());
      }
    });
    
    // Ensure all interactive elements have focus styles
    document.querySelectorAll('a, button, input, select, textarea').forEach(element => {
      element.addEventListener('focus', () => {
        element.classList.add('focus-visible');
      });
      element.addEventListener('blur', () => {
        element.classList.remove('focus-visible');
      });
    });
  }
  
  // Enhance form user experience
  enhanceFormExperience() {
    // Add validation feedback
    document.querySelectorAll('form.needs-validation').forEach(form => {
      const inputs = form.querySelectorAll('input, select, textarea');
      
      inputs.forEach(input => {
        // Visual feedback on input
        input.addEventListener('input', () => {
          if (input.checkValidity()) {
            input.classList.add('is-valid');
            input.classList.remove('is-invalid');
          } else {
            input.classList.remove('is-valid');
            if (input.value) {
              input.classList.add('is-invalid');
            }
          }
        });
      });
    });
    
    // Add auto-growing textareas
    document.querySelectorAll('textarea').forEach(textarea => {
      textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
      });
    });
  }
  
  // Optimize for mobile devices
  addMobileOptimizations() {
    if (window.innerWidth < 768) {
      // Simplify UI on mobile
      document.querySelectorAll('.card').forEach(card => {
        card.classList.add('border-0');
      });
      
      // Ensure buttons have appropriate touch targets
      document.querySelectorAll('.btn-sm').forEach(button => {
        button.classList.remove('btn-sm');
      });
    }
    
    // Handle orientation changes
    window.addEventListener('orientationchange', () => {
      setTimeout(() => {
        if (window.statusChart) window.statusChart.resize();
        if (window.priorityChart) window.priorityChart.resize();
      }, 200);
    });
  }
}

// Initialize UI when the DOM is ready
document.addEventListener('DOMContentLoaded', function() {
  // Initialize theme management
  window.themeManager = new ThemeManager();
  
  // Apply UI enhancements
  window.uiEnhancer = new UIEnhancer();
});