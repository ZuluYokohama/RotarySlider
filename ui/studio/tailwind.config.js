/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        'matrix-bg': '#0d1117',
        'matrix-green': '#3fb950',
        'matrix-blue': '#58a6ff'
      }
    },
  },
  plugins: [],
}
