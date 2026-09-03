import React from "react";

function Cleaning({ data }) {

  if (!data) return null;

  return (
    <section className="result-card">

      <div className="result-card-header">

        <div>
          <span className="phase-label">
            PHASE 02
          </span>

          <h2>Cleaning</h2>

          <p>
            Missing values and duplicate records
          </p>
        </div>

        <span className="completed">
          ✓ Completed
        </span>

      </div>

      <div className="metric-grid">

        <div>
          <span>Original Rows</span>
          <strong>{data.original_rows}</strong>
        </div>

        <div>
          <span>Cleaned Rows</span>
          <strong>{data.cleaned_rows}</strong>
        </div>

        <div>
          <span>Duplicates Removed</span>
          <strong>{data.duplicates_removed}</strong>
        </div>

        <div>
          <span>Missing Before</span>
          <strong>{data.missing_values_before}</strong>
        </div>

        <div>
          <span>Missing After</span>
          <strong>{data.missing_values_after}</strong>
        </div>

      </div>

    </section>
  );
}

export default Cleaning;