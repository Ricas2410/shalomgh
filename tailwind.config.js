/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './custom_admin/templates/**/*.html',
    './core/templates/**/*.html',
    './events/templates/**/*.html',
    './livestream/templates/**/*.html',
    './ministries/templates/**/*.html',
    './pages/templates/**/*.html',
    './sermons/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        'primary-teal': '#008080',
      },
      fontFamily: {
        heading: ['Montserrat', 'sans-serif'],
        body: ['Open Sans', 'sans-serif'],
      },
    },
  },
  plugins: [],
}