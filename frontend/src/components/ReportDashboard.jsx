import Visualization from "./Visualization";
import "./ReportDashboard.css";
import { getReportDownloadUrl } from "../services/api";
function ReportDashboard({ pipelineData }) {
  const phase = (name) => pipelineData?.[name]?.result || pipelineData?.[name] || {};
  const profiling = phase("phase1");
  const cleaning = phase("phase2");
  const eda = phase("phase3");
  const modeling = phase("phase4");
  const visualization = phase("phase5");
  const insights = phase("phase6");
  const missing = Object.values(profiling.missing_values || {}).reduce((total, value) => total + Number(value || 0), 0);
  const observations = insights.insights || insights.observations || [];
  const generatedAt = new Date().toLocaleDateString(undefined, { year: "numeric", month: "long", day: "numeric" });
  const bestModel = modeling.algorithm || "Unavailable";
  const bestScore = modeling.r2_score;

  return (
    <div className="report-dashboard">
      <a
  href={getReportDownloadUrl()}
  className="report-download-btn"
  download
>
  Download Report
</a>
      <header className="report-hero">
        <div>
          <span className="report-kicker">AUTODS / FINAL DELIVERABLE</span>
          <h1>Autonomous Data Scientist Report</h1>
          <p>Evidence-led analysis of the uploaded dataset, from quality assessment through model evaluation and recommendations.</p>
        </div>
        <div className="report-status-badge"><span />Completed</div>
        <dl className="report-meta">
          <div><dt>Dataset</dt><dd>{pipelineData?.filename || "Uploaded CSV dataset"}</dd></div>
          <div><dt>Generated</dt><dd>{generatedAt}</dd></div>
        </dl>
      </header>

      <section className="report-section executive-section">
        <SectionHeading number="01" title="Executive Summary" />
        <div className="executive-grid">
          <div><h3>Overview</h3><p>The dataset contains {profiling.rows ?? 0} rows across {profiling.columns ?? 0} columns. The analysis completed through cleaning, exploration, modeling, visualization, and insight generation.</p></div>
          <div><h3>Most Important Finding</h3><p>{observations[2] || "The analysis produced no additional relationship finding."}</p></div>
          <div><h3>Data Quality</h3><p>{missing} missing value(s) and {profiling.duplicate_rows ?? 0} duplicate row(s) were identified before cleaning.</p></div>
          <div><h3>Modeling</h3><p>{bestModel} achieved an R² score of {formatValue(bestScore)} on the held-out evaluation set.</p></div>
          <div><h3>Recommendation</h3><p>Validate the findings with additional data and cross-validation before operational use.</p></div>
        </div>
      </section>

      <section className="report-section">
        <SectionHeading number="02" title="Key Metrics" />
        <div className="report-kpis">
          <Kpi label="Rows" value={profiling.rows} /><Kpi label="Columns" value={profiling.columns} /><Kpi label="Missing Values" value={missing} /><Kpi label="Duplicate Rows" value={profiling.duplicate_rows ?? 0} /><Kpi label="Numerical Features" value={(profiling.numerical_columns || []).length} /><Kpi label="Categorical Features" value={(profiling.categorical_columns || []).length} /><Kpi label="Best Model" value={bestModel} /><Kpi label="Best Model Score" value={bestScore} />
        </div>
      </section>

      <section className="report-section">
        <SectionHeading number="03" title="Dataset Overview" />
        <ResultTable headers={["Column", "Data Type", "Missing Values", "Unique Values", "Feature Type"]} rows={(profiling.column_names || []).map((column) => [column, profiling.data_types?.[column], profiling.missing_values?.[column] ?? 0, profiling.unique_values?.[column] ?? "Unavailable", (profiling.numerical_columns || []).includes(column) ? "Numerical" : "Categorical"])} />
        <p className="section-interpretation">The table summarizes the schema and feature roles used in downstream analysis.</p>
      </section>

      <section className="report-section">
        <SectionHeading number="04" title="Data Quality Assessment" />
        <ResultTable headers={["Indicator", "Before Cleaning", "After Cleaning"]} rows={[["Rows", profiling.rows, cleaning.cleaned_rows], ["Missing values", missing, cleaning.missing_values_after], ["Duplicate rows", profiling.duplicate_rows ?? 0, 0], ["Feature columns", profiling.columns, profiling.columns]]} />
      </section>

      <section className="report-section">
        <SectionHeading number="05" title="Data Cleaning" />
        <ResultTable headers={["Metric", "Before Cleaning", "After Cleaning", "Change"]} rows={[["Rows", cleaning.original_rows, cleaning.cleaned_rows, `${Number(cleaning.cleaned_rows ?? 0) - Number(cleaning.original_rows ?? 0)}`], ["Missing values", cleaning.missing_values_before, cleaning.missing_values_after, `${Number(cleaning.missing_values_after ?? 0) - Number(cleaning.missing_values_before ?? 0)}`], ["Duplicate rows", cleaning.duplicates_removed, 0, "Removed"]]} />
        <p className="section-interpretation">Duplicate records were removed and missing values were handled using the existing pipeline cleaning rules.</p>
      </section>

      <section className="report-section">
        <SectionHeading number="06" title="Exploratory Data Analysis" />
        <ResultTable headers={["Feature", "Mean", "Median", "Minimum", "Maximum", "Std. Deviation"]} rows={Object.entries(eda.statistics || {}).map(([name, values]) => [name, values.mean, values.median, values.minimum, values.maximum, values.standard_deviation])} />
        <h3 className="subsection-title">Correlation Findings</h3>
        <ResultTable headers={["Feature", ...Object.keys(eda.correlation || {})]} rows={Object.entries(eda.correlation || {}).map(([name, values]) => [name, ...Object.values(values)])} />
      </section>

      <section className="report-section chart-section">
        <SectionHeading number="07" title="Visualization Insights" />
        <Visualization data={visualization} />
      </section>

      <section className="report-section">
        <SectionHeading number="08" title="Modeling Approach" />
        <div className="two-column-copy"><div><h3>Target variable</h3><p>{modeling.target || "Unavailable"}</p></div><div><h3>Features used</h3><p>{modeling.feature || "Unavailable"}</p></div><div><h3>Models evaluated</h3><p>{modeling.algorithm || "Unavailable"}</p></div><div><h3>Evaluation method</h3><p>{modeling.testing_rows ? `${modeling.testing_rows} held-out test rows` : "Unavailable"}</p></div></div>
      </section>

      <section className="report-section">
        <SectionHeading number="09" title="Model Comparison" />
        <ResultTable headers={["Model", "MAE", "RMSE", "R²", "Status"]} rows={[[modeling.algorithm || "Unavailable", modeling.mae, modeling.rmse, modeling.r2_score, "Best available"]]} />
      </section>

      <section className="report-section best-model-section">
        <SectionHeading number="10" title="Best Model" />
        <div className="best-model-card"><span className="best-model-label">SELECTED MODEL</span><strong>{bestModel}</strong><p>Primary evaluation score: <b>{formatValue(bestScore)}</b></p><p>This model is presented because it is the canonical model result produced by the pipeline. Its score should be validated on additional unseen data.</p></div>
      </section>

      <section className="report-section">
        <SectionHeading number="11" title="Model Evaluation" />
        <ResultTable headers={["Metric", "Value"]} rows={[["MAE", modeling.mae], ["RMSE", modeling.rmse], ["R² Score", modeling.r2_score], ["Training rows", modeling.training_rows], ["Testing rows", modeling.testing_rows]]} />
      </section>

      <section className="report-section"><SectionHeading number="12" title="Key Data Insights" /><div className="insight-card-grid">{observations.slice(0, 6).map((observation, index) => <div className="report-insight-card" key={observation}><span>{String(index + 1).padStart(2, "0")}</span><p>{observation}</p></div>)}</div></section>
      <ListSection number="13" title="Business Recommendations" items={["Validate the model using additional unseen data.", "Perform cross-validation before relying on the reported score.", "Use the generated visualizations to review distributions and relationships.", "Add relevant features as more domain data becomes available."]} />
      <ListSection number="14" title="Limitations" items={["The model uses the available numerical feature set.", "Evaluation is based on a single train/test split.", "The dataset size and available context limit generalization conclusions."]} />
      <ListSection number="15" title="Future Improvements" items={["Collect additional representative observations.", "Compare additional model families and tuned configurations.", "Add cross-validation, monitoring, and feature engineering."]} />

      <section className="report-section conclusion-section"><SectionHeading number="16" title="Conclusion" /><p>The uploaded dataset was profiled, cleaned, explored, modeled, visualized, and interpreted successfully. The data contains {profiling.rows ?? 0} rows and {profiling.columns ?? 0} columns, with {profiling.duplicate_rows ?? 0} duplicate row(s) identified during profiling. The strongest reported relationship is reflected in the canonical insights above, while {bestModel} provides the available baseline model result. Further validation with representative unseen data is the main recommendation before production decisions.</p></section>
    </div>
  );
}

function SectionHeading({ number, title }) { return <div className="report-section-heading"><span>{number}</span><h2>{title}</h2></div>; }
function Kpi({ label, value }) { return <div className="report-kpi"><span>{label}</span><strong>{formatValue(value)}</strong></div>; }
function ResultTable({ headers, rows }) { return <div className="report-table-wrap"><table><thead><tr>{headers.map((header) => <th key={header}>{header}</th>)}</tr></thead><tbody>{rows.length ? rows.map((row, index) => <tr key={index}>{row.map((value, cellIndex) => <td key={cellIndex}>{formatValue(value)}</td>)}</tr>) : <tr><td colSpan={headers.length}>No data available.</td></tr>}</tbody></table></div>; }
function ListSection({ number, title, items }) { return <section className="report-section"><SectionHeading number={number} title={title} /><ol className="report-list">{items.map((item) => <li key={item}>{item}</li>)}</ol></section>; }
function formatValue(value) { if (value === null || value === undefined || value === "") return "Unavailable"; if (typeof value === "number") return Number.isFinite(value) ? value.toFixed(4).replace(/\.0000$/, "") : "Unavailable"; return String(value); }

export default ReportDashboard;
