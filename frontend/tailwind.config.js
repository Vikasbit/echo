/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Background layers
        void: '#050816',
        deep: '#0B1020',
        surface: '#111827',
        elevated: '#1F2937',

        // Semantic
        border: 'rgba(255, 255, 255, 0.08)',
        'border-subtle': 'rgba(255, 255, 255, 0.06)',
        'border-hover': 'rgba(255, 255, 255, 0.15)',
        input: 'rgba(255, 255, 255, 0.05)',
        ring: 'rgba(59, 130, 246, 0.5)',

        background: '#050816',
        foreground: '#FFFFFF',

        primary: {
          DEFAULT: '#3B82F6',
          foreground: '#FFFFFF',
        },
        secondary: {
          DEFAULT: '#0B1020',
          foreground: '#A5B4FC',
        },
        accent: {
          DEFAULT: '#8B5CF6',
          foreground: '#FFFFFF',
          blue: '#3B82F6',
          purple: '#8B5CF6',
          cyan: '#06B6D4',
        },
        muted: {
          DEFAULT: '#6B7280',
          foreground: '#9CA3AF',
        },
        destructive: {
          DEFAULT: '#EF4444',
          foreground: '#FFFFFF',
        },
        success: '#22C55E',
        warning: '#F59E0B',
        danger: '#EF4444',

        card: {
          DEFAULT: '#111827',
          foreground: '#FFFFFF',
        },
        popover: {
          DEFAULT: '#111827',
          foreground: '#FFFFFF',
        },
      },
      borderRadius: {
        lg: '1.25rem',
        md: '1rem',
        sm: '0.75rem',
        xl: '1.5rem',
        '2xl': '2rem',
        '3xl': '2.5rem',
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'sans-serif'],
      },
      fontSize: {
        'display-xl': ['5rem', { lineHeight: '1.0', letterSpacing: '-0.03em', fontWeight: '800' }],
        'display-lg': ['3.75rem', { lineHeight: '1.1', letterSpacing: '-0.025em', fontWeight: '700' }],
        'display-md': ['3rem', { lineHeight: '1.15', letterSpacing: '-0.02em', fontWeight: '700' }],
        'heading-lg': ['2.25rem', { lineHeight: '1.2', letterSpacing: '-0.015em', fontWeight: '700' }],
        'heading-md': ['1.5rem', { lineHeight: '1.3', letterSpacing: '-0.01em', fontWeight: '600' }],
        'heading-sm': ['1.25rem', { lineHeight: '1.4', letterSpacing: '-0.005em', fontWeight: '600' }],
        'body-lg': ['1.125rem', { lineHeight: '1.7', fontWeight: '400' }],
        'body-md': ['1rem', { lineHeight: '1.6', fontWeight: '400' }],
        'body-sm': ['0.875rem', { lineHeight: '1.5', fontWeight: '400' }],
        'caption': ['0.75rem', { lineHeight: '1.4', letterSpacing: '0.05em', fontWeight: '500' }],
        'overline': ['0.75rem', { lineHeight: '1.0', letterSpacing: '0.1em', fontWeight: '600' }],
      },
      keyframes: {
        'float': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-12px)' },
        },
        'float-slow': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-8px)' },
        },
        'pulse-glow': {
          '0%, 100%': { opacity: '0.6' },
          '50%': { opacity: '1' },
        },
        'twinkle': {
          '0%, 100%': { opacity: '0.3', transform: 'scale(1)' },
          '50%': { opacity: '1', transform: 'scale(1.2)' },
        },
        'shimmer': {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        'gradient-shift': {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
        'fade-in': {
          from: { opacity: '0' },
          to: { opacity: '1' },
        },
        'fade-up': {
          from: { opacity: '0', transform: 'translateY(30px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
        'scale-in': {
          from: { opacity: '0', transform: 'scale(0.9)' },
          to: { opacity: '1', transform: 'scale(1)' },
        },
        'slide-in-right': {
          from: { transform: 'translateX(100%)' },
          to: { transform: 'translateX(0)' },
        },
        'slide-out-right': {
          from: { transform: 'translateX(0)' },
          to: { transform: 'translateX(100%)' },
        },
        'accordion-down': {
          from: { height: '0', opacity: '0' },
          to: { height: 'var(--accordion-height)', opacity: '1' },
        },
        'accordion-up': {
          from: { height: 'var(--accordion-height)', opacity: '1' },
          to: { height: '0', opacity: '0' },
        },
        'beam-pulse': {
          '0%, 100%': { opacity: '0.4', transform: 'scaleY(1)' },
          '50%': { opacity: '0.8', transform: 'scaleY(1.02)' },
        },
        'orbit': {
          '0%': { transform: 'rotate(0deg) translateX(120px) rotate(0deg)' },
          '100%': { transform: 'rotate(360deg) translateX(120px) rotate(-360deg)' },
        },
      },
      animation: {
        'float': 'float 5s ease-in-out infinite',
        'float-slow': 'float-slow 7s ease-in-out infinite',
        'pulse-glow': 'pulse-glow 4s ease-in-out infinite',
        'twinkle': 'twinkle 3s ease-in-out infinite',
        'shimmer': 'shimmer 3s linear infinite',
        'gradient-shift': 'gradient-shift 6s ease infinite',
        'fade-in': 'fade-in 0.5s ease-out',
        'fade-up': 'fade-up 0.6s cubic-bezier(0.16, 1, 0.3, 1)',
        'scale-in': 'scale-in 0.4s cubic-bezier(0.16, 1, 0.3, 1)',
        'slide-in-right': 'slide-in-right 0.3s ease-out',
        'slide-out-right': 'slide-out-right 0.3s ease-in',
        'accordion-down': 'accordion-down 0.3s ease-out',
        'accordion-up': 'accordion-up 0.3s ease-out',
        'beam-pulse': 'beam-pulse 4s ease-in-out infinite',
        'orbit': 'orbit 20s linear infinite',
      },
      backgroundSize: {
        '400%': '400% 400%',
      },
    },
  },
  plugins: [],
}
