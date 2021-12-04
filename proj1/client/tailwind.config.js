const colors = require("tailwindcss/colors");
module.exports = {
	darkMode: "class",
	purge: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
	theme: {
		extend: {},
		colors: {
			transparent: "transparent",
			current: "currentColor",
			black: colors.black,
			white: colors.white,
			gray: colors.coolGray,
			red: colors.red,
			yellow: colors.amber,
			blue: colors.blue,
			green: colors.green,
		},
	},
	variants: {
		extend: {},
	},
	plugins: [],
};
