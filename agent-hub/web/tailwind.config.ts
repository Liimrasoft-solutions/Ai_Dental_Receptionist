import type { Config } from "tailwindcss";

// Clinical but warm: deep ink, enamel paper, a teal used for links only,
// and four status colors that mean the same thing on every page.
export default {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: { DEFAULT: "#17323A", soft: "#4A5F65", faint: "#7C8D91" },
        paper: "#F4F7F6",
        surface: "#FFFFFF",
        mist: "#E4EDEA",
        line: "#D3DEDA",
        teal: { DEFAULT: "#1D6A73", dark: "#14505A" },
        done: "#2E7D5B",
        staff: "#A9670C",
        failed: "#B3261E",
        waiting: "#647581",
        transferred: "#3B5AA6",
      },
      fontFamily: { sans: ["var(--font-sans)", "system-ui", "sans-serif"] },
      borderRadius: { panel: "6px" },
    },
  },
  plugins: [],
} satisfies Config;
