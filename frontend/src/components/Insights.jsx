import React from "react";

function Insights({ data }) {

  if (!data) return null;

  return (
    <section className="result-card">

      <div className="result-card-header">

        <div>
          <span className="phase-label">
            PHASE 06
          </span>

          <h2>AI Insights</h2>

          <p>
            Automatically generated data insights
          </p>
        </div>

        <span className="completed">
          ✓ Completed
        </span>

      </div>

      <div className="insights-list">

        {data.insights?.map(
          (insight, index) => (

            <div
              className="insight-item"
              key={index}
            >

              <div className="insight-number">
                {String(index + 1).padStart(2, "0")}
              </div>

              <p>
                {insight}
              </p>

            </div>

          )
        )}

      </div>

      {data.correlation !== null &&
        data.correlation !== undefined && (

        <div className="correlation-card">

          <span>
            CORRELATION
          </span>

          <strong>
            {data.correlation.toFixed(4)}
          </strong>

        </div>

      )}

    </section>
  );
}

export default Insights;