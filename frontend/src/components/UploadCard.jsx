import { useRef } from "react";

function UploadSection({
    file,
    setFile,
    onRun,
    loading
}) {

    const inputRef = useRef(null);

    const handleFile = (event) => {

        const selectedFile = event.target.files?.[0];

        if (!selectedFile) return;

        if (!selectedFile.name.toLowerCase().endsWith(".csv")) {
            alert("Please select a CSV file.");
            return;
        }

        setFile(selectedFile);
    };

    return (
        <section className="upload-card">

            <div className="section-label">
                DATASET
            </div>

            <div className="upload-header">

                <div>
                    <h2>Upload Dataset</h2>

                    <p>
                        Upload a CSV file and let AutoDS automatically
                        analyze, clean, model and visualize your data.
                    </p>
                </div>

                <div className="upload-icon">
                    ↑
                </div>

            </div>

            <div
                className="drop-zone"
                onClick={() => inputRef.current?.click()}
            >

                <input
                    ref={inputRef}
                    type="file"
                    accept=".csv"
                    onChange={handleFile}
                    hidden
                />

                <div className="upload-arrow">
                    ↑
                </div>

                <h3>
                    Click to upload CSV
                </h3>

                <p>
                    Only .csv files are supported
                </p>

            </div>

            {file && (

                <div className="selected-file">

                    <div className="file-left">

                        <div className="file-icon">
                            CSV
                        </div>

                        <div>
                            <strong>
                                {file.name}
                            </strong>

                            <span>
                                Dataset ready for analysis
                            </span>
                        </div>

                    </div>

                    <div className="ready-badge">
                        Ready
                    </div>

                </div>

            )}

            <button
                className="run-button"
                disabled={!file || loading}
                onClick={onRun}
            >

                {loading ? (
                    <>
                        <span className="button-spinner"></span>
                        Running AutoDS...
                    </>
                ) : (
                    <>
                        Run AutoDS
                        <span>→</span>
                    </>
                )}

            </button>

        </section>
    );
}

export default UploadSection;