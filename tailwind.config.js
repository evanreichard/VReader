/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./vreader/templates/**/*.html", "./vreader/assets/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        primary: "var(--color-primary)",
        secondary: "var(--color-secondary)",
        tertiary: "var(--color-tertiary)",
        ptext: "var(--color-primary-text)",
        stext: "var(--color-secondary-text)",
      },
    },
  },
  plugins: [],
};
