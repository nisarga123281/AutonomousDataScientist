import React from "react";

function EDA({ data }) {

  if (!data) return null;

  return (
    <section className="result-card">

      <div className="result-card-header">

        <div>
          <span className="phase-label">
            PHASE 03
          </span>

          <h2>Exploratory Data Analysis</h2>

          <p>
            Statistical understanding of your dataset
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
          <span>Numerical Columns</span>
          <strong>
            {data.numerical_columns?.length || 0}
          </strong>
        </div>

        <div>
          <span>Categorical Columns</span>
          <strong>
            {data.categorical_columns?.length || 0}
          </strong>
        </div>

      </div>

      {data.statistics && (

        <div className="table-container">

          <h3>Numerical Statistics</h3>

          <table>

            <thead>
              <tr>
                <th>Column</th>
                <th>Mean</th>
                <th>Median</th>
                <th>Minimum</th>
                <th>Maximum</th>
                <th>Std. Dev.</th>
              </tr>
            </thead>

            <tbody>

              {Object.entries(data.statistics).map(
                ([column, stats]) => (

                  <tr key={column}>

                    <td>{column}</td>
                    <td>{stats.mean.toFixed(2)}</td>
                    <td>{stats.median.toFixed(2)}</td>
                    <td>{stats.minimum.toFixed(2)}</td>
                    <td>{stats.maximum.toFixed(2)}</td>
                    <td>{stats.standard_deviation.toFixed(2)}</td>

                  </tr>

                )
              )}

            </tbody>

          </table>

        </div>

      )}

    </section>
  );
}

export default EDA;