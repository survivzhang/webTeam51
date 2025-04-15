/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        // 🌐 Primary brand color
        primary: {
          DEFAULT: "#3B82F6", // Primary blue – for buttons, links, and highlights
          light: "#E0ECFF", // Light blue – for backgrounds, hovers, or subtle accents
        },

        // 💜 Secondary accent color
        secondary: {
          DEFAULT: "#8B5CF6", // Lavender – for tags, highlights, or secondary CTAs
          light: "#EDE9FE", // Light lavender – for soft backgrounds or hover effects
        },

        // 💚 Success/Accent color
        accent: {
          DEFAULT: "#10B981", // Mint green – used for success states or active indicators
          light: "#D1FAE5", // Light mint – background for success messages or badges
        },

        // 🪟 Layout and structure
        background: "#F8FAFC", // Base background – light gray-blue for page backgrounds
        card: "#FFFFFF", // Card and component surface – clean white
        border: "#E5E7EB", // Optional: subtle borders (e.g., for dividers or cards)
        shadow: "rgba(0, 0, 0, 0.05)", // Optional: light shadow for elevation

        // ✍️ Text and UI content
        text: "#111827", // Main text – dark gray for high readability
        muted: "#64748B", // Muted text – for secondary info, labels, descriptions
        disabled: "#9CA3AF", // Optional: for disabled text or inputs
        link: "#3B82F6", // Hyperlinks – often matches primary

        // 🔔 Feedback and status
        success: "#22C55E", // Success messages, checkmarks
        error: "#EF4444", // Errors, alerts, invalid states
        warning: "#F59E0B", // Warnings, caution notes
        info: "#3B82F6", // Informational notes (can reuse primary)
      },
    },
  },
  plugins: [],
};
