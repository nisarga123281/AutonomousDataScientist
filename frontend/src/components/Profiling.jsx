import React from "react";

function Profiling({ data }) {

  if (!data) return null;

  return (
    <section className="result-card">

      <div className="result-card-header">

        <div>
          <span className="phase-label">
            PHASE 01
          </span>

          <h2>Profiling</h2>

          <p>
            Dataset structure and quality overview
          </p>
        </div>

        <span className="completed">
          ✓ Completed
        </span>

      </div>

      <div className="metric-grid">

        <div>
          <span>Rows</span>
          <strong>{data.rows}</strong>
        </div>

        <div>
          <span>Columns</span>
          <strong>{data.columns}</strong>
        </div>

        <div>
          <span>Numerical</span>
          <strong>
            {data.numerical_columns?.length || 0}
          </strong>
        </div>

        <div>
          <span>Categorical</span>
          <strong>
            {data.categorical_columns?.length || 0}
          </strong>
        </div>

      </div>

      <div className="column-list">

        <h3>Columns</h3>

        <div className="tags">

          {data.column_names?.map(column => (
            <span key={column}>
              {column}
            </span>
          ))}

        </div>

      </div>

    </section>
  );
}

export default Profiling;