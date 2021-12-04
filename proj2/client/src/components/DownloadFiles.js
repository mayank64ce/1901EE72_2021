import React from "react";
import axios from "axios";

const handleSubmitClick = (event, url, alert) => {
	event.preventDefault();

	axios
		.get(url)
		.then((res) => {
			console.log("SUCCESS downloading !!");
			if ("Download" in res.data) {
				console.log(res.data["Download"]);
				Window.open(res.data["Download"], "_blank");
				// alert.show(res.data["Info"]);
			}
			if ("Success" in res.data) {
				alert.success(res.data["Success"]);
			}
			if ("Error" in res.data) {
				alert.error(res.data["Error"]);
			}
		})
		.catch(function () {
			console.log("FAILURE couldn't download !!");
		});
};

function DownloadFiles({ baseUrl, endpoint, alert }) {
	const url = `${baseUrl}${endpoint}`;
	return (
		<div>
			<button
				className="btn-blue"
				onClick={(e) => handleSubmitClick(e, url, alert)}
			>
				Download generated files
			</button>
		</div>
	);
}

export default DownloadFiles;
