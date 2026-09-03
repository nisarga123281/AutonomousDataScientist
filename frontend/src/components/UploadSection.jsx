import { useState } from "react";
import { UploadCloud, FileSpreadsheet, Play, LoaderCircle } from "lucide-react";
import { runAutoDS } from "../services/api";

function UploadSection({ setPipelineData }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0];

    if (!selectedFile) return;

    if (!selectedFile.name.toLowerCase().endsWith(".csv")) {
      setError("Only CSV files are supported.");
      setFile(null);
      return;
    }

    setError("");
    setFile(selectedFile);
  };

  const handleRun = async () => {
    if (!file) {
      setError("Please upload a CSV file first.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const result = await runAutoDS(file);

      setPipelineData(result);
    } catch (err) {
      setError(
        err?.message || "Failed to run AutoDS."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="upload-section">

      <div className="upload-card">

        {/* TOP */}

        <div className="upload-content">

          <div className="upload-icon">
            <UploadCloud size={25} />
          </div>

          <div>

            <h2>
              Upload Dataset
            </h2>

            <p>
              Upload your dataset and let AutoDS automatically
              profile, clean, analyze, model and generate insights.
            </p>

          </div>

        </div>


        {/* DROP AREA */}

        <label className="upload-box">

          <input
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            hidden
          />

          <div className="upload-box-icon">
            <UploadCloud size={30} />
          </div>

          <strong>
            Click to upload your CSV dataset
          </strong>

          <small>
            Supported format: .CSV
          </small>

        </label>


        {/* SELECTED FILE */}

        {file && (

          <div className="selected-file">

            <div className="selected-file-left">

              <div className="file-type-icon">
                <FileSpreadsheet size={18} />
              </div>

              <div>

                <strong>
                  {file.name}
                </strong>

                <small>
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </small>

              </div>

            </div>

            <span className="ready">
              READY
            </span>

          </div>

        )}


        {/* ERROR */}

        {error && (
          <div className="upload-error">
            {error}
          </div>
        )}


        {/* RUN */}

        <button
          className="run-button"
          onClick={handleRun}
          disabled={loading || !file}
        >

          {loading ? (
            <>
              <LoaderCircle
                size={17}
                className="loading-icon"
              />

              Running AutoDS...
            </>
          ) : (
            <>
              <Play size={16} />

              Run AutoDS
            </>
          )}

        </button>

      </div>

    </section>
  );
}

export default UploadSection;