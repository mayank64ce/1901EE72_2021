import React, { useState, useEffect } from "react";
import DarkModeToggle from "react-dark-mode-toggle";

export default function DarkMode({ alert }) {
	const [isDarkMode, setIsDarkMode] = useState(() => false);

	useEffect(() => {
		// On page load or when changing themes, best to add inline in `head` to avoid FOUC
		if (
			localStorage.theme === "dark" ||
			(!("theme" in localStorage) &&
				window.matchMedia("(prefers-color-scheme: dark)").matches)
		) {
			document.documentElement.className = "light";
			alert.show("Welcome to the Light side!");
			console.log("light");
		} else {
			document.documentElement.className = "dark";
			alert.show("Join the Dark side!");
			console.log("dark");
		}

		if (isDarkMode) localStorage.theme = "dark";
		else localStorage.theme = "light";
	}, [isDarkMode]);

	return (
		<DarkModeToggle
			onChange={setIsDarkMode}
			checked={isDarkMode}
			size={80}
		/>
	);
}
