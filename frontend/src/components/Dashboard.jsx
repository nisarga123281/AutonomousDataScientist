import UploadSection from "./UploadSection";
import Pipeline from "./Pipeline";
function Dashboard({ setPage, pipelineData, setPipelineData }) {

  const isCompleted =
    pipelineData?.workflow_status === "completed";

  const phase1 = pipelineData?.phase1 || {};
  const phase4 = pipelineData?.phase4 || {};
  const phase6 = pipelineData?.phase6 || {};
  const phase1Result = phase1.result || phase1;
  const phase6Result = phase6.result || phase6;

  const rows = phase1Result.rows ?? 0;
  const columns = phase1Result.columns ?? 0;

  const missingValues = phase1Result.missing_values
    ? Object.values(phase1Result.missing_values).reduce(
        (total, value) => total + value,
        0
      )
    : 0;

  const duplicates = phase1Result.duplicate_rows ?? 0;

  const dataQuality =
    rows > 0
      ? Math.max(
          0,
          Math.round(
            100 -
              ((missingValues + duplicates) / rows) * 100
          )
        )
      : 0;

  const insights =
    Array.isArray(phase6Result.insights || phase6Result.observations)
      ? (phase6Result.insights || phase6Result.observations)
      : [];

  return (
    <div className="dashboard-page">

      {/* =================================================
          HERO
      ================================================= */}

      <section className="dashboard-hero">

        <div className="hero-content">

          <div className="eyebrow">
            AUTONOMOUS DATA SCIENCE PLATFORM
          </div>

          <h1>
            Smart Data.
            <span> Automated Insights.</span>
          </h1>

          <p>
            Upload your dataset and let the autonomous pipeline do the rest —
            from profiling to final report.
          </p>

          <div className="hero-meta">

            <div className="online-status">
              <span className="status-dot"></span>
              SYSTEM ONLINE
            </div>

            <div className="hero-divider"></div>

            <span>7 AUTONOMOUS STAGES</span>

            <div className="hero-divider"></div>

            <span>END-TO-END ANALYSIS</span>

          </div>

        </div>

      </section>


      {/* =================================================
          DATASET WORKSPACE
      ================================================= */}

      <section className="workspace-section">

        <div className="section-heading">

          <div>

            <span className="eyebrow">
              DATASET WORKSPACE
            </span>

            <h2>
              Analyze your dataset
            </h2>

            <p>
              Upload a CSV file and let AutoDS execute the
              complete autonomous data science pipeline.
            </p>

          </div>

          {isCompleted && (
            <div className="run-status">

              <span className="status-dot"></span>

              ANALYSIS COMPLETED

            </div>
          )}

        </div>

        <UploadSection
          setPipelineData={setPipelineData}
        />

      </section>


      {/* =================================================
          DATASET OVERVIEW
      ================================================= */}

      {pipelineData && (
        <section className="dataset-overview">

          <div className="section-heading compact">

            <div>

              <span className="eyebrow">
                DATASET INTELLIGENCE
              </span>

              <h2>
                Dataset Overview
              </h2>

            </div>

            <button
              className="results-button"
              onClick={() => setPage("results")}
            >
              View Results →
            </button>

          </div>


          <div className="dashboard-overview-layout">

            {/* DATASET INFORMATION */}

            <div className="dataset-info-card">

              <div className="dataset-card-title">

                <span className="dataset-file-icon">
                  ▤
                </span>

                <div>

                  <strong>
                    Dataset
                  </strong>

                  <small>
                    Processed successfully
                  </small>

                </div>

                <span className="processed-badge">
                  Processed
                </span>

              </div>


              <div className="dataset-details">

                <div>
                  <span>Rows</span>
                  <strong>{rows.toLocaleString()}</strong>
                </div>

                <div>
                  <span>Columns</span>
                  <strong>{columns}</strong>
                </div>

                <div>
                  <span>Missing</span>
                  <strong>{missingValues}</strong>
                </div>

                <div>
                  <span>Duplicates</span>
                  <strong>{duplicates}</strong>
                </div>

              </div>

            </div>


            {/* METRIC CARDS */}

            <div className="metric-grid">

              {/* DATA QUALITY */}

              <div className="metric-card">

                <h3>
                  Data Quality
                </h3>

                <div className="metric-ring quality-ring">

                  <div>
                    <strong>
                      {dataQuality}%
                    </strong>

                    <small>
                      Quality
                    </small>
                  </div>

                </div>

                <span>
                  {dataQuality >= 95
                    ? "High Quality"
                    : "Needs Review"}
                </span>

              </div>


              {/* MISSING VALUES */}

              <div className="metric-card">

                <h3>
                  Missing Values
                </h3>

                <strong className="metric-number">
                  {missingValues}
                </strong>

                <small>
                  {rows > 0
                    ? `${(
                        (missingValues / rows) *
                        100
                      ).toFixed(2)}%`
                    : "0%"}
                </small>

                <span>
                  {missingValues === 0
                    ? "None Found"
                    : "Needs Attention"}
                </span>

              </div>


              {/* DUPLICATES */}

              <div className="metric-card">

                <h3>
                  Duplicates
                </h3>

                <strong className="metric-number">
                  {duplicates}
                </strong>

                <small>
                  {rows > 0
                    ? `${(
                        (duplicates / rows) *
                        100
                      ).toFixed(2)}%`
                    : "0%"}
                </small>

                <span>
                  {duplicates === 0
                    ? "None Found"
                    : "Detected"}
                </span>

              </div>


              {/* DATA INSIGHTS */}

              <div className="metric-card">

                <h3>
                  Data Insights
                </h3>

                <strong className="metric-number">
                  {insights.length}
                </strong>

                <small>
                  Key Findings
                </small>

                <span>
                  AI Generated
                </span>

              </div>


              {/* MODEL */}

              <div className="metric-card">

                <h3>
                  Model Accuracy
                </h3>

                <div className="metric-ring model-ring">

                  <div>

                    <strong>
                      {phase4?.metrics?.r2_score != null
                        ? `${(
                            phase4.metrics.r2_score * 100
                          ).toFixed(1)}%`
                        : "—"}
                    </strong>

                    <small>
                      R² Score
                    </small>

                  </div>

                </div>

                <span>
                  Model Performance
                </span>

              </div>

            </div>

          </div>

        </section>
      )}


      {/* =================================================
          AUTONOMOUS PIPELINE
      ================================================= */}

      <section className="pipeline-section">

        <div className="section-heading compact">

          <div>

            <span className="eyebrow">
              AUTONOMOUS WORKFLOW
            </span>

            <h2>
              Autonomous Workflow
            </h2>

            <p>
              Seven specialized stages work together to
              transform raw data into actionable intelligence.
            </p>

          </div>

          <div className="pipeline-count">
            07 STAGES
          </div>

        </div>

        <Pipeline
          pipelineData={pipelineData}
        />

      </section>


      {/* =================================================
          LATEST ANALYSIS + KEY INSIGHTS
      ================================================= */}

      <section className="bottom-dashboard-grid">

        {/* KEY INSIGHTS */}

        <div className="key-insights-card">

          <div className="bottom-card-header">

            <div>

              <span className="eyebrow">
                AI GENERATED
              </span>

              <h2>
                Key Insights
              </h2>

            </div>

            <span className="insight-bulb">
              ✦
            </span>

          </div>


          {insights.length > 0 ? (

            <div className="insights-list">

              {insights.slice(0, 5).map(
                (insight, index) => (

                  <div
                    className="insight-item"
                    key={index}
                  >

                    <span className="insight-check">
                      ✓
                    </span>

                    <p>
                      {typeof insight === "string"
                        ? insight
                        : insight?.text || insight?.message || "Insight available"}
                    </p>

                  </div>

                )
              )}

            </div>

          ) : (

            <div className="no-insights">
              Run AutoDS to generate AI-powered
              dataset insights.
            </div>

          )}

        </div>

      </section>

    </div>
  );
}

export default Dashboard;
