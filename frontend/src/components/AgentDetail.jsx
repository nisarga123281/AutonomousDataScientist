import Visualization from "./Visualization";
import ReportDashboard from "./ReportDashboard";
import "./AgentDetail.css";

const stageNames = [
  "Profiling",
  "Cleaning",
  "EDA",
  "Modeling",
  "Visualization",
  "AI Insights",
  "Report",
];

function AgentDetail({ agent, onBack, pipelineData }) {
  if (!agent) return null;

  const phaseKey = `phase${Number(agent.id)}`;
  const phaseData = pipelineData?.[phaseKey] || {};
  const result = phaseData.result || phaseData;
  const summaryLines = buildSummaryLines(agent.name, result);
  const warnings = phaseData.warnings || [];
  const recommendations = phaseData.recommendations || [];

  return (
    <div className="agent-detail-page">
      <button className="back-btn" onClick={onBack}>← Back to Pipeline</button>

      <section className="agent-detail-header">
        <div>
          <div className="detail-label">AUTODS PIPELINE • STAGE {agent.id}</div>
          <h1>{agent.name} — {phaseData.status === "completed" ? "Completed" : "Ready"}</h1>
          <p>{agent.description}</p>
        </div>
        <div className="detail-status"><span className="status-dot" />{phaseData.status === "completed" ? "COMPLETED" : "READY"}</div>
      </section>

      <section className="detail-results-panel">
        <div className="section-title"><span>RESULTS</span><small>TABLES / CARDS / CHARTS</small></div>
        {renderResults(agent.name, result, phaseData, pipelineData)}
      </section>

      <section className="detail-section detail-summary-section">
        <div className="section-title"><span>SUMMARY</span><small>6 POINTS</small></div>
        <ol className="summary-lines">
          {summaryLines.map((line) => <li key={line}>{line}</li>)}
        </ol>
      </section>

      {warnings.length > 0 && <section className="detail-section"><div className="section-title"><span>WARNINGS</span></div><ul>{warnings.map((warning) => <li key={warning}>{warning}</li>)}</ul></section>}
      {recommendations.length > 0 && <section className="detail-section"><div className="section-title"><span>RECOMMENDATIONS</span></div><ul>{recommendations.map((recommendation) => <li key={recommendation}>{recommendation}</li>)}</ul></section>}

      <section className="flow-section">
        <div className="section-title"><span>AUTONOMOUS PIPELINE</span><small>7 STAGES</small></div>
        <div className="agent-flow">{stageNames.map((stage, index) => <div key={stage} className={stage === agent.name ? "flow-stage active" : "flow-stage"}><span>{String(index + 1).padStart(2, "0")}</span>{stage}</div>)}</div>
      </section>
    </div>
  );
}

function renderResults(stage, result, phaseData, pipelineData) {
  if (stage === "Profiling") return <ProfilingResults result={result} status={phaseData.status} />;
  if (stage === "Cleaning") return <ResultTable headers={["Metric", "Before", "After"]} rows={[["Rows", result.original_rows, result.cleaned_rows], ["Duplicate rows", result.duplicates_removed, 0], ["Missing values", result.missing_values_before, result.missing_values_after]]} />;
  if (stage === "EDA") return <><ResultTable headers={["Feature", "Mean", "Median", "Minimum", "Maximum", "Std. Deviation"]} rows={Object.entries(result.statistics || {}).map(([name, values]) => [name, values.mean, values.median, values.minimum, values.maximum, values.standard_deviation])} /><h3>Correlation Matrix</h3><ResultTable headers={["Feature", ...Object.keys(result.correlation || {})]} rows={Object.entries(result.correlation || {}).map(([name, values]) => [name, ...Object.values(values)])} /></>;
  if (stage === "Modeling") return <ResultTable headers={["Model", "MAE", "RMSE", "R² Score", "Feature", "Target"]} rows={[[result.algorithm, result.mae, result.rmse, result.r2_score, result.feature, result.target]]} />;
  if (stage === "Visualization") return <Visualization data={result} />;
  if (stage === "AI Insights") return <div className="insight-cards">{(result.insights || result.observations || []).map((insight) => <div className="insight-card" key={insight}>{insight}</div>)}</div>;
  if (stage === "Report") return <ReportDashboard pipelineData={pipelineData} />;
  return <p>No structured results available.</p>;
}

function ProfilingResults({ result, status }) {
  const missing = Object.values(result.missing_values || {}).reduce((total, value) => total + Number(value || 0), 0);
  const columns = result.column_names || [];
  return <>
    <ResultTable headers={["Metric", "Value"]} rows={[["Rows", result.rows], ["Columns", result.columns], ["Duplicate Rows", result.duplicate_rows ?? 0], ["Status", status || "completed"]]} />
    <h3>Column Information</h3>
    <ResultTable headers={["Column Name", "Data Type", "Missing Values", "Category"]} rows={columns.map((column) => [column, result.data_types?.[column], result.missing_values?.[column] ?? 0, (result.numerical_columns || []).includes(column) ? "Numerical" : "Categorical"])} />
    <h3>Numerical Columns</h3><p>{(result.numerical_columns || []).join(" • ") || "None"}</p>
    <h3>Categorical Columns</h3><p>{(result.categorical_columns || []).join(" • ") || "None"}</p>
    <span className="result-note">Total missing values: {missing}</span>
  </>;
}

function ResultTable({ headers, rows }) {
  return <div className="result-table-wrap"><table><thead><tr>{headers.map((header) => <th key={header}>{header}</th>)}</tr></thead><tbody>{rows.length ? rows.map((row, rowIndex) => <tr key={rowIndex}>{row.map((value, cellIndex) => <td key={cellIndex}>{formatValue(value)}</td>)}</tr>) : <tr><td colSpan={headers.length}>No structured results available.</td></tr>}</tbody></table></div>;
}

function formatValue(value) {
  if (value === null || value === undefined) return "—";
  if (Array.isArray(value)) return `${value.length} item(s)`;
  if (typeof value === "object") return "Available";
  return String(value);
}

function buildSummaryLines(stage, result) {
  const missing = Object.values(result.missing_values || {}).reduce((total, value) => total + Number(value || 0), 0);
  const observations = result.insights || result.observations || [];
  const plots = result.generated_plots || [];
  const lines = {
    Profiling: [`The dataset contains ${result.rows ?? 0} rows.`, `The dataset contains ${result.columns ?? 0} columns.`, `${(result.numerical_columns || []).length} numerical columns were identified.`, `${(result.categorical_columns || []).length} categorical columns were identified.`, `${missing} missing value(s) were detected.`, `${result.duplicate_rows ?? 0} duplicate row(s) were detected.`],
    Cleaning: [`The source dataset contained ${result.original_rows ?? 0} rows.`, `${result.duplicates_removed ?? 0} duplicate row(s) were removed.`, `The cleaned dataset contains ${result.cleaned_rows ?? 0} rows.`, `${result.missing_values_before ?? 0} missing value(s) existed before cleaning.`, `${result.missing_values_after ?? 0} missing value(s) remain after cleaning.`, "Missing values were handled using the available column values."],
    EDA: [`Descriptive statistics cover ${(result.numerical_columns || []).length} numerical column(s).`, `${(result.categorical_columns || []).length} categorical column(s) were reviewed.`, `${Object.keys(result.statistics || {}).length} feature statistic set(s) were generated.`, `${Object.keys(result.correlation || {}).length} correlation row(s) were calculated.`, `${missing} missing value(s) remain in the analyzed data.`, "The EDA results are available for interpretation."],
    Modeling: [`The selected model is ${result.algorithm || "not available"}.`, `The model used ${result.training_rows ?? 0} training row(s).`, `The evaluation used ${result.testing_rows ?? 0} testing row(s).`, `The R² score is ${result.r2_score ?? "not available"}.`, `The MAE is ${result.mae ?? "not available"}.`, `The RMSE is ${result.rmse ?? "not available"}.`],
    Visualization: [`${plots.length} interactive Plotly chart(s) were generated.`, `${plots.filter((plot) => plot.type === "histogram").length} distribution chart(s) were generated.`, `${plots.filter((plot) => plot.type === "scatter").length} relationship chart(s) were generated.`, `${plots.filter((plot) => plot.type === "boxplot").length} outlier chart(s) were generated.`, `${plots.filter((plot) => plot.type === "heatmap").length} correlation heatmap(s) were generated.`, "The charts use the uploaded dataset for interactive exploration."],
    "AI Insights": [`${observations.length} insight(s) were generated.`, `${missing} missing value(s) were included in the quality findings.`, `${result.duplicate_rows ?? 0} duplicate row(s) were included in the findings.`, `The reported correlation is ${result.correlation ?? "not available"}.`, "The findings are based on the canonical pipeline results.", "The findings are ready for the final report."],
    Report: ["The report consolidates the completed pipeline stages.", "Dataset profiling and quality findings are included.", "Cleaning and exploratory analysis results are included.", "Model evaluation and visualization findings are included.", "Insights and recommendations are included.", "The final conclusion is available in this report."],
  };
  return lines[stage] || ["Results are available.", "The stage completed.", "Structured data was processed.", "The output is ready.", "Findings are available.", "The pipeline can continue."];
}

export default AgentDetail;
