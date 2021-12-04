import React from "react";
import axios from "axios";

const handleButtonClick = (event, url, alert) => {
	event.preventDefault();

	axios
		.get(url)
		.then((res) => {
			console.log("SUCCESS generating concise !!");
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
			console.log("FAILURE generating concise !!");
		});
};

export default function GenConciseMarksheet({ baseUrl, endpoint, alert }) {
	const url = `${baseUrl}${endpoint}`;

	return (
		<>
			<button
				className="btn-blue"
				onClick={(e) => handleButtonClick(e, url, alert)}
			>
				Generate concise marksheet
			</button>
		</>
	);
}
