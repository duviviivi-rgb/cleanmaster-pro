/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1E88E5',
        secondary: '#64B5F6',
        accent: '#0D47A1',
        success: '#4CAF50',
        warning: '#FFC107',
        danger: '#F44336',
        dark: '#121212',
        light: '#F5F5F5'
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}