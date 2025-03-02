// Shader-inspired color system for improved UI
class ColorSystem {
  constructor() {
    this.darkMode = localStorage.getItem('darkMode') === 'true';
    this.createToggleButton();
    this.applyColorMode();
    
    // Generate dynamic CSS variables based on primary color
    this.generateColorPalette();
  }
  
  createToggleButton() {
    this.button = document.createElement('button');
    this.button.className = 'btn btn-sm btn-outline-secondary position-fixed top-0 end-0 m-3';
    this.button.textContent = this.darkMode ? '☀️ Light' : '🌙 Dark';
    this.button.addEventListener('click', () => this.toggleDarkMode());
    document.body.appendChild(this.button);
  }
  
  toggleDarkMode() {
    this.darkMode = !this.darkMode;
    this.applyColorMode();
    this.button.textContent = this.darkMode ? '☀️ Light' : '🌙 Dark';
    localStorage.setItem('darkMode', this.darkMode);
  }
  
  applyColorMode() {
    document.body.classList.toggle('dark-mode', this.darkMode);
    // Apply shader-inspired background
    if (this.darkMode) {
      document.body.style.background = 'linear-gradient(135deg, #1a1f25 0%, #2d3748 100%)';
      document.body.style.color = '#f7fafc';
    } else {
      document.body.style.background = 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)';
      document.body.style.color = '#212529';
    }
  }
  
  // Use color theory to generate a cohesive palette
  generateColorPalette() {
    // Base colors derived from shader-like calculations
    const primaryBase = getComputedStyle(document.documentElement).getPropertyValue('--primary').trim() || '#4a6ed0';
    
    // Convert to RGB for shader-like calculations
    const rgb = this.hexToRgb(primaryBase);
    if (!rgb) return;
    
    // Generate color variations using shader-like techniques
    const root = document.documentElement;
    
    // Primary color variations (like shader mix() function)
    root.style.setProperty('--primary-light', this.lighten(rgb, 0.2));
    root.style.setProperty('--primary-dark', this.darken(rgb, 0.2));
    
    // Complementary color (like shader calculations)
    const complementary = this.calculateComplementary(rgb);
    root.style.setProperty('--complementary', this.rgbToHex(complementary));
    
    // Analogous colors (like shader rotations)
    const analogous1 = this.rotateHue(rgb, 30);
    const analogous2 = this.rotateHue(rgb, -30);
    root.style.setProperty('--analogous-1', this.rgbToHex(analogous1));
    root.style.setProperty('--analogous-2', this.rgbToHex(analogous2));
    
    // Apply these colors to cards based on status
    this.applyStatusColors();
  }
  
  // Apply generated colors to status badges and UI elements
  applyStatusColors() {
    // Status badges with shader-inspired gradients
    const badges = document.querySelectorAll('.badge');
    badges.forEach(badge => {
      if (badge.classList.contains('bg-success')) {
        badge.style.background = 'linear-gradient(to right, #28a745, #20c997)';
      } else if (badge.classList.contains('bg-warning')) {
        badge.style.background = 'linear-gradient(to right, #ffc107, #fd7e14)';
      } else if (badge.classList.contains('bg-danger')) {
        badge.style.background = 'linear-gradient(to right, #dc3545, #e74c3c)';
      } else if (badge.classList.contains('bg-info')) {
        badge.style.background = 'linear-gradient(to right, #17a2b8, #0dcaf0)';
      } else if (badge.classList.contains('bg-secondary')) {
        badge.style.background = 'linear-gradient(to right, #6c757d, #adb5bd)';
      }
      badge.style.border = 'none';
    });
    
    // Cards with subtle gradients
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
      if (this.darkMode) {
        card.style.background = 'linear-gradient(145deg, #2d3748 0%, #1a202c 100%)';
        card.style.borderColor = '#4a5568';
      } else {
        card.style.background = 'linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%)';
        card.style.borderColor = '#dee2e6';
      }
      card.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.05)';
    });
    
    // Buttons with enhanced gradients
    const buttons = document.querySelectorAll('.btn-primary');
    buttons.forEach(button => {
      button.style.background = 'linear-gradient(to right, var(--primary), var(--primary-dark))';
      button.style.borderColor = 'var(--primary-dark)';
    });
  }
  
  // Color utility functions (inspired by shader operations)
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
  
  lighten({r, g, b}, amount) {
    return this.rgbToHex({
      r: Math.min(255, Math.floor(r + (255 - r) * amount)),
      g: Math.min(255, Math.floor(g + (255 - g) * amount)),
      b: Math.min(255, Math.floor(b + (255 - b) * amount))
    });
  }
  
  darken({r, g, b}, amount) {
    return this.rgbToHex({
      r: Math.max(0, Math.floor(r * (1 - amount))),
      g: Math.max(0, Math.floor(g * (1 - amount))),
      b: Math.max(0, Math.floor(b * (1 - amount)))
    });
  }
  
  calculateComplementary({r, g, b}) {
    // Similar to shader invert operation
    return {r: 255 - r, g: 255 - g, b: 255 - b};
  }
  
  rotateHue({r, g, b}, degrees) {
    // Convert RGB to HSL
    const {h, s, l} = this.rgbToHsl({r, g, b});
    
    // Rotate hue (like in GLSL)
    let newHue = h + degrees;
    if (newHue < 0) newHue += 360;
    if (newHue >= 360) newHue -= 360;
    
    // Convert back to RGB
    return this.hslToRgb({h: newHue, s, l});
  }
  
  rgbToHsl({r, g, b}) {
    r /= 255;
    g /= 255;
    b /= 255;
    
    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    let h, s, l = (max + min) / 2;
    
    if (max === min) {
      h = s = 0; // achromatic
    } else {
      const d = max - min;
      s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
      
      switch (max) {
        case r: h = (g - b) / d + (g < b ? 6 : 0); break;
        case g: h = (b - r) / d + 2; break;
        case b: h = (r - g) / d + 4; break;
      }
      
      h /= 6;
    }
    
    return {h: h * 360, s, l};
  }
  
  hslToRgb({h, s, l}) {
    h /= 360;
    let r, g, b;
    
    if (s === 0) {
      r = g = b = l; // achromatic
    } else {
      const hue2rgb = (p, q, t) => {
        if (t < 0) t += 1;
        if (t > 1) t -= 1;
        if (t < 1/6) return p + (q - p) * 6 * t;
        if (t < 1/2) return q;
        if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
        return p;
      };
      
      const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
      const p = 2 * l - q;
      
      r = hue2rgb(p, q, h + 1/3);
      g = hue2rgb(p, q, h);
      b = hue2rgb(p, q, h - 1/3);
    }
    
    return {
      r: Math.round(r * 255),
      g: Math.round(g * 255),
      b: Math.round(b * 255)
    };
  }
}

// Subtle element enhancements
class SubtleEnhancements {
  constructor() {
    this.enhanceInputs();
    this.enhanceButtons();
    this.enhanceBadges();
  }
  
  enhanceInputs() {
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
      // Add subtle transition on focus
      input.addEventListener('focus', () => {
        input.style.boxShadow = '0 0 0 3px rgba(74, 110, 208, 0.2)';
        input.style.transition = 'box-shadow 0.2s ease-in-out';
      });
      
      input.addEventListener('blur', () => {
        input.style.boxShadow = '';
      });
    });
  }
  
  enhanceButtons() {
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
      // Add subtle hover effect
      button.addEventListener('mouseenter', () => {
        button.style.transform = 'translateY(-1px)';
        button.style.transition = 'transform 0.2s ease-in-out';
      });
      
      button.addEventListener('mouseleave', () => {
        button.style.transform = '';
      });
    });
  }
  
  enhanceBadges() {
    const badges = document.querySelectorAll('.badge');
    badges.forEach(badge => {
      // Improve badge readability
      badge.style.fontWeight = '500';
      badge.style.letterSpacing = '0.5px';
      badge.style.padding = '0.4em 0.6em';
    });
  }
}

// Initialize the color system and enhancements
document.addEventListener('DOMContentLoaded', function() {
  // Apply shader-inspired color system
  new ColorSystem();
  
  // Add subtle UI enhancements
  new SubtleEnhancements();
});