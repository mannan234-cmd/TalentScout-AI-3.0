/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#eef4ff",
          100: "#d9e6ff",
          200: "#b3ccff",
          300: "#82abff",
          400: "#5285ff",
          500: "#2f5eff",
          600: "#1c40e6",
          700: "#1731b4",
          800: "#152a8c",
          900: "#142670",
        },
      },
    },
  },
  plugins: [],
}
