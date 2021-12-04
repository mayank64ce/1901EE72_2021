import React from "react";
import Basic from "./Basic";
const axios = require("axios");

const handleSubmitClick = (event, url, reqFile, alert) => {
	event.preventDefault();

	const formData = new FormData();
	console.log(reqFile);
	// console.log(event.target[0].files);
	// console.log(event.target[0].files[0]);
	formData.append("file", reqFile);
	// console.log(formData);
	axios
		.post(url, formData, {
			headers: {
				"Content-Type": "multipart/form-data",
			},
		})
		.then((res) => {
			console.log("SUCCESS!!");
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
			console.log("FAILURE!!");
		});
};

export default function UploadFileComp({ baseUrl, endpoint, text, alert }) {
	const url = `${baseUrl}${endpoint}`;

	return (
		<>
			<h3 className="h3-tag">{text}</h3>
			<div className="flex m-2 items-center">
				<Basic url={url} handleSubmitClick={handleSubmitClick} alert={alert} />
			</div>
		</>
	);
}
