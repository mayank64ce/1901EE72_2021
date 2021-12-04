import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

export default function Basic({ url, handleSubmitClick, alert }) {
	const [reqFile, setReqFile] = useState(null);
	const onDrop = useCallback((acceptedFiles) => {
		// console.log(acceptedFiles);
		setReqFile(acceptedFiles[0]);
	}, []);
	const {
		// acceptedFiles,
		getRootProps,
		getInputProps,
		isDragActive,
		// rejectedFiles,
	} = useDropzone({
		onDrop,
	});

	// console.log(reqFile);

	// const files = acceptedFiles.map((file) => (
	// 	<li key={file.path}>
	// 		{file.path} - {file.size} bytes
	// 	</li>
	// ));

	// console.log(rejectedFiles);

	return (
		<div className="w-1/2">
			<form
				encType="multipart/form-data"
				onSubmit={(event) =>
					handleSubmitClick(event, url, reqFile, alert)
				}
			>
				<div
					{...getRootProps({
						className: "dnd-area",
						onDrop: (event) => event.preventDefault(),
						// className:
						// 	" flex-auto border rounded border-opacity-100 border-blue-500",
					})}
				>
					<input {...getInputProps()} />

					{isDragActive ? (
						<p>Drop files here</p>
					) : (
						<p>
							Drag 'n' drop some files here, or click to select
							files
						</p>
					)}

					{/* <Basic />
					 */}
				</div>
				<aside>
					{/* {reqFile.length ? <h4></h4> : null} */}
					{reqFile ? (
						<ul>
							<li key={reqFile.path}>
								{reqFile.path} - {reqFile.size} bytes{" "}
							</li>
						</ul>
					) : null}
				</aside>
				<input type="submit" value="Submit" className="btn-green" />
			</form>
		</div>
	);
}
