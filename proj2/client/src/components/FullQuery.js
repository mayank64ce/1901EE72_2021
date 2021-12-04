import React from "react";
import axios from "axios";

const handleSubmitClick = (event, url, alert) => {
	event.preventDefault();

	axios
		.get(url)
		.then((res) => {
			console.log("SUCCESS generating full !!");
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
			console.log("FAILURE generating full !!");
		});
};

export default function FullQuery({ baseUrl, endpoint, alert }) {
	const url = `${baseUrl}${endpoint}`;
	return (
		<>
			<button
				className="btn-blue"
				onClick={(e) => handleSubmitClick(e, url, alert)}
			>
				Generate all transcripts
			</button>
		</>
	);
}
