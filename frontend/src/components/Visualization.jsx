const API_BASE_URL = "http://127.0.0.1:8000";

export default function Visualization({ data }) {
  if (!data) {
    return (
      <section className="dashboard-card">
        <div className="section-header">
          <div>
            <span className="phase-label">PHASE 05</span>
            <h2>Visualization</h2>
            <p>Visual understanding of your dataset</p>
          </div>
        </div>

        <div className="empty-state">
          <div className="empty-icon">▥</div>
          <h3>No visualizations available</h3>
          <p>Run the AutoDS analysis to generate charts.</p>
        </div>
      </section>
    );
  }

  const plots = data.generated_plots || [];

  const getPlotTitle = (plot) => {
    const name = plot.name.replace(/\.html$/i, "");
    const readableName = name
      .replace(/_histogram$/, "")
      .replace(/_boxplot$/, "")
      .replace(/_vs_/g, " vs ")
      .replace(/_/g, " ")
      .replace(/\b\w/g, (character) => character.toUpperCase());

    if (plot.type === "histogram") {
      return `${readableName} Distribution`;
    }

    if (plot.type === "scatter") {
      return readableName;
    }

    if (plot.type === "heatmap") {
      return "Correlation Heatmap";
    }

    if (plot.type === "boxplot") {
      return `${readableName} Distribution and Outliers`;
    }

    if (plot.type === "bar_chart") {
      return `${readableName} Category Distribution`;
    }

    return "Data Visualization";
  };

  const getPlotDescription = (plot) => {
    if (plot.type === "histogram") {
      return "Inspect the observed distribution and frequency of values.";
    }

    if (plot.type === "scatter") {
      return "Explore the relationship between the dataset's numerical variables.";
    }

    if (plot.type === "heatmap") {
      return "Compare correlations across the available numerical variables.";
    }

    if (plot.type === "boxplot") {
      return "Review spread, median, and potential outliers in the data.";
    }

    if (plot.type === "bar_chart") {
      return "Compare observed counts across the dataset categories.";
    }

    return "Explore this interactive view of the uploaded dataset.";
  };

  return (
    <section className="dashboard-card visualization-section">
      <div className="section-header">
        <div>
          <span className="phase-label">PHASE 05</span>

          <h2>Visualization</h2>

          <p>
            Interactive visual understanding of your dataset
          </p>
        </div>

        <div className="section-status">
          <span className="status-dot"></span>
          Completed
        </div>
      </div>

      {/* Visualization summary */}

      <div className="visualization-summary">
        <div className="mini-stat">
          <span className="mini-stat-label">Library</span>
          <strong>{data.library || "Plotly"}</strong>
        </div>

        <div className="mini-stat">
          <span className="mini-stat-label">Charts Generated</span>
          <strong>{data.plots_generated || plots.length}</strong>
        </div>

        <div className="mini-stat">
          <span className="mini-stat-label">Interactive</span>
          <strong>Yes</strong>
        </div>
      </div>

      {/* Charts */}

      {plots.length > 0 ? (
        <div className="visualization-grid">
          {plots.map((plot, index) => (
            <div className="chart-card" key={`${plot.name}-${index}`}>
              <div className="chart-header">
                <div>
                  <span className="chart-number">
                    {String(index + 1).padStart(2, "0")}
                  </span>

                  <h3>{getPlotTitle(plot)}</h3>

                  <p>{getPlotDescription(plot)}</p>
                </div>

                <span className="chart-type">
                  {plot.type}
                </span>
              </div>

              <div className="chart-container">
                <iframe
                  src={`${API_BASE_URL}${plot.url}`}
                  title={plot.name}
                  loading="lazy"
                />
              </div>

              <div className="chart-footer">
                <span>Interactive Plotly Visualization</span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <div className="empty-icon">📊</div>

          <h3>No charts generated</h3>

          <p>
            AutoDS could not generate visualizations for this dataset.
          </p>
        </div>
      )}
    </section>
  );
}
