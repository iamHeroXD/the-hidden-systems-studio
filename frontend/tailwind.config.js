/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        studio: {
          950: "#080B11",
          900: "#0D131F",
          850: "#131B2B",
          800: "#1A2438",
          700: "#24324D",
          600: "#384B6E",
          chalk: "#E2E8F0",
          muted: "#94A3B8",
          amber: "#F59E0B",
          teal: "#06B6D4",
          crimson: "#EF4444",
          emerald: "#10B981"
        }
      },
      fontFamily: {
        mono: ["ui-monospace", "SFMono-Regular", "Menlo", "Monaco", "Consolas", "monospace"],
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "sans-serif"]
      }
    },
  },
  plugins: [],
};
