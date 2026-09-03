import React from "react";

function Modeling({ data }) {

  return (
    <section className="result-card">

      <div className="result-card-header">

        <div>
          <span className="phase-label">
            PHASE 04
          </span>

          <h2>Modeling</h2>

          <p>
            Machine learning model performance
          </p>
        </div>

        <span className="completed">
          ✓ Completed
        </span>

      </div>

      {!data ? (

        <div className="model-warning">

          <div className="warning-icon">
            !
          </div>

          <div>

            <strong>
              Modeling unavailable
            </strong>

            <p>
              The dataset does not contain enough
              numerical columns to train the current
              regression model.
            </p>

          </div>

        </div>

      ) : (

        <>

          <div className="model-name">
            <span>Algorithm</span>
            <strong>
              {data.algorithm}
            </strong>
          </div>

          <div className="model-flow">

            <div>
              <span>Feature</span>
              <strong>{data.feature}</strong>
            </div>

            <div className="model-arrow">
              →
            </div>

            <div>
              <span>Target</span>
              <strong>{data.target}</strong>
            </div>

          </div>

          <div className="metric-grid">

            <div>
              <span>Training Rows</span>
              <strong>{data.training_rows}</strong>
            </div>

            <div>
              <span>Testing Rows</span>
              <strong>{data.testing_rows}</strong>
            </div>

            <div>
              <span>MAE</span>
              <strong>{data.mae?.toFixed(3)}</strong>
            </div>

            <div>
              <span>RMSE</span>
              <strong>{data.rmse?.toFixed(3)}</strong>
            </div>

            <div>
              <span>R² Score</span>
              <strong>{data.r2_score?.toFixed(3)}</strong>
            </div>

          </div>

          <div className="equation">

            <span>MODEL EQUATION</span>

            <code>
              {data.target} ={" "}
              {data.coefficient?.toFixed(3)}
              {" × "}
              {data.feature}
              {" "}
              {data.intercept >= 0 ? "+" : "-"}{" "}
              {Math.abs(data.intercept)?.toFixed(3)}
            </code>

          </div>

        </>

      )}

    </section>
  );
}

export default Modeling;