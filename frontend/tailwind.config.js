/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark_orange: "#ff914d",
        light_orange: "#fec0a7",
      },
      keyframes: {
        hop: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-10px)" },
        },
      },
      animation: {
        hop: "hop 1.5s infinite ease-in-out",
      },
    },
  },
  plugins: [],
};
