import React, { useEffect } from "react";
import RangeQuery from "./components/RangeQuery";
import FullQuery from "./components/FullQuery";
import UploadFileComp from "./components/UploadFileComp";
import DownloadFiles from "./components/DownloadFiles";
import axios from "axios";
import { useAlert } from "react-alert";

const baseUrl = "http://localhost:5002";
export default function App() {
	useEffect(() => {
		axios.get(`${baseUrl}/deleteResidualOutput`).then((res) => {
			console.log(res.data);
		});
	}, []);

	const alert = useAlert();

	return (
		<div className="container mx-auto px-10">
			<div className="flex text-center items-center justify-center place-content-center ">
				<h1 className="h1-tag my-3 mb-7">Transcript Generator</h1>
			</div>
			<div className="flex flex-auto items-center content-center md:content-around justify-center p-2 m-0.5 border border-opacity-100 border-black rounded-lg">
				<div>
					<div className="grid grid-cols-1 md:grid-cols-3 sm:grid-cols-2">
						<div className="my-2">
							<UploadFileComp
								baseUrl={baseUrl}
								endpoint={"/upload/grades"}
								text="Upload grades.csv:"
								alert={alert}
							/>
						</div>
						<div className="my-2">
							<UploadFileComp
								baseUrl={baseUrl}
								endpoint={"/upload/stud_roll"}
								text="Upload stud_roll.csv:"
								alert={alert}
							/>
						</div>
						<div className="my-2">
							<UploadFileComp
								baseUrl={baseUrl}
								endpoint={"/upload/subject_master"}
								text="Upload subject_master.csv:"
								alert={alert}
							/>
						</div>
						<div className="my-2">
							<UploadFileComp
								baseUrl={baseUrl}
								endpoint={"/upload/seal"}
								text="Upload SEAL:"
								alert={alert}
							/>
						</div>
						<div className="my-2">
							<UploadFileComp
								baseUrl={baseUrl}
								endpoint={"/upload/signature/"}
								text="Upload Signature:"
								alert={alert}
							/>
						</div>
					</div>

					<div className="flex m-5 items-top my-8">
						<div>
							<RangeQuery
								baseUrl={baseUrl}
								endpoint={"/query/range/"}
								alert={alert}
							/>
						</div>
						<div className="my-14 py-6 mx-5">
							<FullQuery
								baseUrl={baseUrl}
								endpoint={"/query/full/"}
								alert={alert}
							/>
						</div>
						<div className="my-14 py-6 mx-5">
							<DownloadFiles
								baseUrl={baseUrl}
								endpoint={"/downloadzip/"}
								alert={alert}
							/>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}
