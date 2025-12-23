/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'gold': {
          DEFAULT: '#D4AF37',
          50: '#FBF6E8',
          100: '#F5EAC8',
          200: '#EDD99A',
          300: '#E5C76B',
          400: '#D4AF37',
          500: '#B8962E',
          600: '#9A7D26',
          700: '#7C641E',
          800: '#5E4B16',
          900: '#40320E',
        },
        'vermilion': {
          DEFAULT: '#C41E3A',
          50: '#FDE8EC',
          100: '#FAC5CE',
          200: '#F59DAD',
          300: '#E63950',
          400: '#C41E3A',
          500: '#9A1830',
          600: '#7A1326',
          700: '#5A0E1C',
          800: '#3A0912',
          900: '#1A0408',
        },
        'ink': {
          DEFAULT: '#1F1F1F',
          50: '#4A4A4A',
          100: '#3D3D3D',
          200: '#333333',
          300: '#2D2D2D',
          400: '#262626',
          500: '#1F1F1F',
          600: '#181818',
          700: '#121212',
          800: '#0D0D0D',
          900: '#080808',
        },
        'rice': {
          DEFAULT: '#F7F4ED',
          50: '#FFFFFF',
          100: '#FDFCFA',
          200: '#F7F4ED',
          300: '#EDE8DC',
          400: '#E3DCCB',
          500: '#D9D0BA',
        },
        'jade': {
          DEFAULT: '#00A86B',
          light: '#2ECC71',
          dark: '#008B57',
        },
      },
      fontFamily: {
        'serif-cn': ['"Noto Serif SC"', '"Source Han Serif SC"', 'serif'],
        'sans-cn': ['"Noto Sans SC"', 'sans-serif'],
      },
      boxShadow: {
        'glow-gold': '0 0 20px rgba(212, 175, 55, 0.3)',
        'glow-vermilion': '0 0 20px rgba(196, 30, 58, 0.4)',
        'glow-jade': '0 0 20px rgba(0, 168, 107, 0.3)',
        'inner-gold': 'inset 0 0 20px rgba(212, 175, 55, 0.1)',
        'pillar': '0 4px 20px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(212, 175, 55, 0.2)' },
          '100%': { boxShadow: '0 0 20px rgba(212, 175, 55, 0.4)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
}
