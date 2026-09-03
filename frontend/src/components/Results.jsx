import {
  Database,
  AlertTriangle,
  Copy,
  Columns3,
  Sparkles,
  BrainCircuit,
  BarChart3,
  FileText,
  CheckCircle2,
} from "lucide-react";

function Results({ pipelineData }) {

  if (!pipelineData) {
    return (
      <div className="results-page empty-results">

        <div className="empty-results-icon">
          <Database size={32} />
        </div>

        <h1>No Analysis Yet</h1>

        <p>
          Upload a CSV dataset from the dashboard and run AutoDS
          to see your analysis results here.
        </p>

      </div>
    );
  }


  const phase1 = pipelineData.phase1 || {};
  const phase2 = pipelineData.phase2 || {};
  const phase3 = pipelineData.phase3 || {};
  const phase4 = pipelineData.phase4 || {};
  const phase5 = pipelineData.phase5 || {};
  const phase6 = pipelineData.phase6 || {};
  const phase7 = pipelineData.phase7 || {};

  const phaseResult = (phase) => phase.result || phase;
  const profileResult = phaseResult(phase1);
  const cleaningResult = phaseResult(phase2);
  const edaResult = phaseResult(phase3);
  const visualizationResult = phaseResult(phase5);
  const insightsResult = phaseResult(phase6);
  const reportResult = phaseResult(phase7);


  const missingValues = profileResult.missing_values
    ? Object.values(profileResult.missing_values)
        .reduce((total, value) => total + Number(value || 0), 0)
    : 0;


  const insights = insightsResult.insights || insightsResult.observations || [];


  return (
    <div className="results-page">

      {/* HEADER */}

      <div className="results-header">

        <div>

          <span className="eyebrow">
            AUTODS ANALYSIS
          </span>

          <h1>
            Analysis Results
          </h1>

          <p>
            Complete autonomous data science analysis generated
            by the AutoDS agent pipeline.
          </p>

        </div>

        <div className="results-completed">
          <CheckCircle2 size={16} />
          PIPELINE COMPLETED
        </div>

      </div>


      {/* DATASET SUMMARY */}

      <section className="results-section">

        <div className="results-section-title">

          <div className="results-title-icon">
            <Database size={19} />
          </div>

          <div>
            <span>PHASE 01</span>
            <h2>Dataset Profiling</h2>
          </div>

        </div>


        <div className="results-stats">

          <ResultStat
            icon={<Database size={18} />}
            label="ROWS"
            value={profileResult.rows ?? "—"}
          />

          <ResultStat
            icon={<Columns3 size={18} />}
            label="COLUMNS"
            value={profileResult.columns ?? "—"}
          />

          <ResultStat
            icon={<AlertTriangle size={18} />}
            label="MISSING VALUES"
            value={missingValues}
          />

          <ResultStat
            icon={<Copy size={18} />}
            label="DUPLICATES"
            value={profileResult.duplicate_rows ?? 0}
          />

        </div>


        {/* COLUMNS */}

        {profileResult.column_names?.length > 0 && (

          <div className="column-list-card">

            <div className="column-list-header">
              <span>DATASET COLUMNS</span>
              <small>
                {profileResult.column_names.length} features
              </small>
            </div>

            <div className="column-list">

              {profileResult.column_names.map((column) => (

                <div
                  className="column-chip"
                  key={column}
                >
                  {column}
                </div>

              ))}

            </div>

          </div>

        )}

      </section>


      {/* CLEANING */}

      <section className="results-section">

        <ResultHeader
          icon={<Sparkles size={19} />}
          phase="PHASE 02"
          title="Data Cleaning"
        />

        <div className="cleaning-grid">

          <MetricBox
            label="ORIGINAL ROWS"
            value={cleaningResult.original_rows ?? "—"}
          />

          <MetricBox
            label="CLEANED ROWS"
            value={cleaningResult.cleaned_rows ?? "—"}
          />

          <MetricBox
            label="DUPLICATES REMOVED"
            value={cleaningResult.duplicates_removed ?? 0}
          />

        </div>

      </section>


      {/* EDA */}

      <section className="results-section">

        <ResultHeader
          icon={<BarChart3 size={19} />}
          phase="PHASE 03"
          title="Exploratory Data Analysis"
        />

        <div className="eda-info">

          <div>
            <span>NUMERICAL FEATURES</span>

            <strong>
              {edaResult.numerical_columns?.length ?? 0}
            </strong>
          </div>

          <div>
            <span>CATEGORICAL FEATURES</span>

            <strong>
              {edaResult.categorical_columns?.length ?? 0}
            </strong>
          </div>

        </div>

      </section>


      {/* MODEL */}

      <section className="results-section">

        <ResultHeader
          icon={<BrainCircuit size={19} />}
          phase="PHASE 04"
          title="Modeling"
        />

        <div className="model-result">

          <div className="model-status">
            <CheckCircle2 size={18} />
            Model analysis completed
          </div>

          {Object.keys(phase4.metrics || {}).length > 0 && (

            <div className="metrics-grid">

              {Object.entries(phase4.metrics).map(
                ([key, value]) => (

                  <div
                    className="model-metric"
                    key={key}
                  >

                    <span>
                      {key.replaceAll("_", " ").toUpperCase()}
                    </span>

                    <strong>
                      {typeof value === "number"
                        ? value.toFixed(4)
                        : String(value)}
                    </strong>

                  </div>

                )
              )}

            </div>

          )}

        </div>

      </section>
          {/* VISUALIZATIONS */}

        <section className="results-section">

        <ResultHeader
            icon={<BarChart3 size={19} />}
            phase="PHASE 05"
            title="Data Visualizations"
        />

        <VisualizationGallery phase5={visualizationResult} />

        </section>

      {/* AI INSIGHTS */}

      <section className="results-section insights-section">

        <ResultHeader
          icon={<Sparkles size={19} />}
          phase="PHASE 06"
          title="AI Insights"
        />

        {insights.length > 0 ? (

          <div className="insights-list">

            {insights.map((insight, index) => (

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

            ))}

          </div>

        ) : (

          <div className="no-data">
            No AI insights were returned.
          </div>

        )}

      </section>


      {/* REPORT */}

      <section className="results-section">

        <ResultHeader
          icon={<FileText size={19} />}
          phase="PHASE 07"
          title="Final Report"
        />

        <div className="report-card">

          <div className="report-status">

            <CheckCircle2 size={18} />

            <div>
              <strong>
                AutoDS Report Generated
              </strong>

              <small>
                Complete analysis report is ready.
              </small>
            </div>

          </div>


          {(phase7.summary || reportResult.summary) && (

            <div className="report-summary">
              {phase7.summary || reportResult.summary}
            </div>

          )}

          {(phase7.report_file || reportResult.report_file) && (

            <div className="report-file">
              Report generated successfully
            </div>

          )}

        </div>

      </section>

    </div>
  );
}

function VisualizationGallery({ phase5 }) {

  const plots =
    phase5?.generated_plots ||
    phase5?.plots ||
    phase5?.visualizations ||
    phase5?.files ||
    [];

  if (!plots.length) {
    return (
      <div className="no-data">
        No visualizations were generated.
      </div>
    );
  }

  return (
    <div className="visualization-grid">

      {plots.map((plot, index) => {

        const plotPath =
          typeof plot === "string"
            ? plot
            : plot?.path ||
              plot?.url ||
              plot?.file;

        if (!plotPath) return null;

        const fullUrl =
          plotPath.startsWith("http")
            ? plotPath
            : `http://127.0.0.1:8000${
                plotPath.startsWith("/")
                  ? ""
                  : "/"
              }${plotPath}`;

        const isHtml =
          plotPath.toLowerCase().endsWith(".html");

        return (
          <div
            className="visualization-card"
            key={index}
          >

            <div className="visualization-header">

              <span>
                VISUALIZATION{" "}
                {String(index + 1).padStart(2, "0")}
              </span>

              <span className="visualization-type">
                {isHtml ? "INTERACTIVE" : "CHART"}
              </span>

            </div>

            <div className="visualization-content">

              {isHtml ? (

                <iframe
                  src={fullUrl}
                  title={`Visualization ${index + 1}`}
                />

              ) : (

                <img
                  src={fullUrl}
                  alt={`Visualization ${index + 1}`}
                />

              )}

            </div>

          </div>
        );

      })}

    </div>
  );
}
/* =========================================================
   COMPONENTS
   ========================================================= */

function ResultStat({ icon, label, value }) {
  return (
    <div className="result-stat">

      <div className="result-stat-icon">
        {icon}
      </div>

      <span>{label}</span>

      <strong>{value}</strong>

    </div>
  );
}


function MetricBox({ label, value }) {
  return (
    <div className="metric-box">

      <span>{label}</span>

      <strong>{value}</strong>

    </div>
  );
}


function ResultHeader({ icon, phase, title }) {
  return (
    <div className="results-section-title">

      <div className="results-title-icon">
        {icon}
      </div>

      <div>
        <span>{phase}</span>
        <h2>{title}</h2>
      </div>

    </div>
  );
}

export default Results;