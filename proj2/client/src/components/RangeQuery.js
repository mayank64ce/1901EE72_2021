import { React, useState } from "react";
import axios from "axios";

const handleSubmitClick = (event, url, data, alert, setAbsent) => {
	event.preventDefault();

	axios
		.post(url, data, {
			headers: {
				"Content-Type": "Application/json",
			},
		})
		.then((res) => {
			console.log("SUCCESS generating rannge !!");
			console.log(res.data);
			if ("Success" in res.data) {
				alert.success(res.data["Success"]);
			}
			if ("Info" in res.data) {
				alert.show("some roll numbers were absent");
				setAbsent(
					res.data["Info"].map(
						(element) => <li key={element}>{element}</li>
						// alert.show(res.data["Info"]);
					)
				);
			}
			if ("Error" in res.data) {
				alert.error(res.data["Error"]);
			}
		})
		.catch(function () {
			console.log("FAILURE generating rannge !!");
		});
};

export default function RangeQuery({ baseUrl, endpoint, alert }) {
	const [rangeFrom, setRangeFrom] = useState("0401CS01");
	const [rangeTo, setRangeTo] = useState("0401CS99");

	const [absent, setAbsent] = useState(null);
	const url = `${baseUrl}${endpoint}`;
	const rangeData = {
		from: {
			rangeFrom,
		},
		to: {
			rangeTo,
		},
	};

	return (
		<>
			<div className="flex-auto justify-center items-center border border-opacity-100 rounded-lg">
				<form
					encType="multipart/form-data"
					onSubmit={(event) =>
						handleSubmitClick(
							event,
							url,
							rangeData,
							alert,
							setAbsent
						)
					}
				>
					<label>
						<h3 className="h3-tag  m-2">
							{" "}
							Enter range of roll numbers:
						</h3>
						<div>
							<input
								type="text"
								className="classic-input m-2"
								value={rangeFrom}
								onChange={(e) => {
									setRangeFrom(e.target.value);
									console.log(e.target.value);
								}}
							></input>
							<input
								type="text"
								className="classic-input  m-2"
								value={rangeTo}
								onChange={(e) => {
									setRangeTo(e.target.value);
									console.log(e.target.value);
								}}
							></input>
						</div>
					</label>
					<input
						type="submit"
						value="Generate transcripts for range"
						className="btn-blue  m-2"
					/>
				</form>
			</div>
			{absent ? (
				<aside>
					<h3 className="h3-tag"> Absent roll numbers:</h3>
					<ul className="collapse list-unstyled">{absent}</ul>
				</aside>
			) : null}
		</>
	);
}
