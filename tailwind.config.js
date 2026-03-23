/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './sections/cc-*.liquid',
    './sections/cc-pdp-*.liquid',
    './snippets/cc-*.liquid',
  ],
  theme: {
    extend: {
      colors: {
        'parchment': '#FAF9F6',
        'deep-ink': '#0A0A0A',
        'warm-gray': '#6B6B6B',
        'light-gray': '#E8E8E8',
        'forest': '#1A3A2F',
        'forest-light': '#2D5A47',
        'ocean': '#062F3D',
        'brand-navy': '#1E2D4D',
      },
      fontFamily: {
        'grotesk': ['Space Grotesk', 'system-ui', 'sans-serif'],
        'inter': ['Inter', 'system-ui', 'sans-serif'],
      }
    }
  },
  corePlugins: {
    preflight: false,
  },
}
