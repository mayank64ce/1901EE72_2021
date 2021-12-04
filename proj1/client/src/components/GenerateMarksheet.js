import React from "react";
import axios from "axios";

const handleButtonClick = (event, url, data, alert) => {
	event.preventDefault();

	axios
		.post(url, data, {
			headers: {
				"Content-Type": "Application/json",
			},
		})
		.then((res) => {
			console.log("SUCCESS generating marksheet !!");
			console.log(res.data);
			if ("Success" in res.data) {
				alert.success(res.data["Success"]);
			}
			if ("Info" in res.data) {
				alert.show(res.data["Info"]);
			}
			if ("Error" in res.data) {
				alert.error(res.data["Error"]);
			}
		})
		.catch(function () {
			console.log("FAILURE generating marksheet !!");
		});
};

export default function GenerateMarksheet({
	baseUrl,
	endpoint,
	posMark,
	negMark,
	alert,
}) {
	const url = `${baseUrl}${endpoint}`;
	const markingData = {
		positive: {
			posMark,
		},
		negative: {
			negMark,
		},
	};

	return (
		<>
			<button
				className="btn-blue"
				onClick={(e) => handleButtonClick(e, url, markingData, alert)}
			>
				Generate Roll Number wise marksheet
			</button>
		</>
	);
}
