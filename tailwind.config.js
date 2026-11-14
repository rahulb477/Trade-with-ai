/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ['class'],
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          950: '#080D19',
          900: '#101827',
          800: '#111C2D',
          700: '#1A273D',
          600: '#24344E',
        },
        brand: {
          DEFAULT: '#667AFF',
          hover: '#5267F5',
          soft: 'rgba(102, 122, 255, 0.14)',
        },
        signal: {
          success: '#16B995',
          danger: '#F16F83',
          warning: '#F5B841',
          entry: '#4C9AFF',
        },
        ink: {
          DEFAULT: '#E8EDF7',
          muted: '#8D9AB0',
          subtle: '#607089',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace'],
      },
      boxShadow: {
        card: '0 8px 30px rgba(0, 0, 0, 0.32)',
      },
    },
  },
  plugins: [],
};
