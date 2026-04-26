/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        parchment: {
          50:  "#fdf8f0",
          100: "#f5e6c8",
          200: "#e8cc99",
          300: "#d4a96a",
          400: "#c8943f",
        },
        gold: {
          300: "#f0c040",
          400: "#d4a017",
          500: "#b8860b",
          600: "#8b6508",
        },
        brown: {
          800: "#1a0f00",
          900: "#110a00",
          950: "#0a0500",
        },
        tavern: {
          bg:      "#120c04",
          surface: "#1e1208",
          card:    "#241608",
          border:  "#6b4c1e",
          glow:    "#d4a01720",
        }
      },
      fontFamily: {
        heading: ["Cinzel", "serif"],
        body:    ["Crimson Text", "serif"],
      },
      boxShadow: {
        gold:    "0 0 12px 2px #d4a01730, inset 0 0 20px #d4a01710",
        "gold-sm": "0 0 6px 1px #d4a01720",
      }
    },
  },
  plugins: [],
}