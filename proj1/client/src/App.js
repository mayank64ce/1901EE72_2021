import { React, useState, useEffect } from "react";
// import "./App.css";
import UploadFileComponent from "./components/UploadFileComponent";
import GenerateMarksheet from "./components/GenerateMarksheet.js";
import GenConciseMarksheet from "./components/GenConciseMarksheet";
import SendEmail from "./components/SendEmail";
import DarkMode from "./components/DarkMode";
import { useAlert } from "react-alert";
import axios from "axios";
const baseUrl = "http://127.0.0.1:5000";

export default function App() {
	const [posMark, setPosMark] = useState(0);
	const [negMark, setNegMark] = useState(0);

	useEffect(() => {
		if (
			localStorage.theme === "dark" ||
			(!("theme" in localStorage) &&
				window.matchMedia("(prefers-color-scheme: dark)").matches)
		) {
			document.documentElement.className = "dark";
			console.log("dark");
		} else {
			document.documentElement.className = "light";
			console.log("light");
		}

		axios.get(`${baseUrl}/deleteResidualOutput`).then((res) => {
			console.log(res.data);
		});
	}, []);

	const alert = useAlert();

	return (
		<div className="transition duration-500 ease-in-out bg-white dark:bg-gray-800 dark:text-white h-screen flex flex-grow">
			<div className="flex-auto items-center justify-center rounded p-2 m-0.5">
				<div className="flex flex-auto">
					<h1 className="h1-tag my-3 mb-7 flex-grow items-center justify-center text-center">
						Marksheet Generator
					</h1>
					<div>
						<DarkMode alert={alert} />
					</div>
				</div>
				<div className="container ">
					<div>
						<h3 className="h3-tag">Upload master csv:</h3>
						<UploadFileComponent
							baseUrl={baseUrl}
							endpoint="/upload/master/"
							alert={alert}
						/>
					</div>
					<div>
						<h3 className="h3-tag">Upload responses csv:</h3>
						<UploadFileComponent
							baseUrl={baseUrl}
							endpoint="/upload/responses/"
							alert={alert}
						/>
					</div>
					<div>
						<h3 className="h3-tag">Enter marking scheme:</h3>
						<div className="flex m-4 items-center">
							<div>
								<label>
									Correct answer:
									<input
										className="classic-input"
										type="text"
										value={posMark}
										name="positive marks"
										onChange={(e) => {
											setPosMark(e.target.value);
											console.log(e.target.value);
										}}
									/>
								</label>
							</div>
							<div>
								<label>
									Wrong answer:
									<input
										className="classic-input"
										type="text"
										value={negMark}
										name="negative marks"
										onChange={(e) =>
											setNegMark(e.target.value)
										}
									/>
								</label>
							</div>
						</div>
					</div>

					<div>
						<h3 className="h3-tag">Get output:</h3>
						<div className="flex m-4 items-center">
							<div>
								<GenerateMarksheet
									baseUrl={baseUrl}
									endpoint={"/output/marksheet/"}
									posMark={posMark}
									negMark={negMark}
									alert={alert}
								/>
							</div>

							<div>
								<GenConciseMarksheet
									baseUrl={baseUrl}
									endpoint={"/output/concise-marksheet/"}
									alert={alert}
								/>
							</div>
							<div>
								<SendEmail
									baseUrl={baseUrl}
									endpoint={"/send-email/"}
									alert={alert}
								/>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}
