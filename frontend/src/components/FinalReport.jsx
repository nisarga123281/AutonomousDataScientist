import React from "react";

function FinalReport({ data }) {

  if (!data) return null;

  return (
    <section className="report-card">

      <div className="report-icon">
        ▤
      </div>

      <div className="report-content">

        <span className="phase-label">
          PHASE 07
        </span>

        <h2>
          Final Report
        </h2>

        <p>
          Complete automated data science report
        </p>

        <div className="report-status">
          ✓ Report generated successfully
        </div>

        <a
          className="report-button"
          href={`http://127.0.0.1:8000${data.report_file}`}
          target="_blank"
          rel="noreferrer"
        >
          View Final Report
          <span>→</span>
        </a>

      </div>

    </section>
  );
}

export default FinalReport;