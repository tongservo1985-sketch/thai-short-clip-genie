import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          primary: "#6366f1", // Indigo
          secondary: "#a855f7", // Purple
          accent: "#f43f5e", // Rose (for Thai "Hot" trends)
          dark: "#0f172a",
        },
      },
      fontFamily: {
        sans: ['var(--font-kanit)', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
export default config;