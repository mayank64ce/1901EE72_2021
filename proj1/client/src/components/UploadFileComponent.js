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
			// if ("Success" in res.data) {
			// 	alert.success(res.data["Success"]);
			// }
			// if ("Info" in res.data) {
			// 	alert.show(res.data["Info"]);
			// }
			// if ("Error" in res.data) {
			// 	alert.error(res.data["Error"]);
			// }
			console.log(res.data);
			console.log(res.data["Success"]);
			if ("Success" in res.data) {
				alert.success(res.data["Success"]);
			}
			if ("Info" in res.data) {
				console.log(res.data["Info"]);
				alert.show(res.data["Info"]);
			}
			if ("Error" in res.data) {
				console.log(res.data["Error"]);
				alert.error(res.data["Error"]);
			}
		})
		.catch(function (f) {
			console.log("FAILURE!!", f);
		});
};

export default function UploadFileComponent({ baseUrl, endpoint, alert }) {
	const url = `${baseUrl}${endpoint}`;

	return (
		<div className="flex m-2 items-center">
			<Basic
				url={url}
				handleSubmitClick={handleSubmitClick}
				alert={alert}
			/>
		</div>
	);
}
