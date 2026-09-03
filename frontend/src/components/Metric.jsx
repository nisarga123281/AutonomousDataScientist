function Metric({
  title,
  value,
  description,
}) {
  return (
    <div className="metric">

      <span className="metric-title">
        {title}
      </span>

      <strong className="metric-value">
        {value ?? "—"}
      </strong>

      {description && (
        <span className="metric-description">
          {description}
        </span>
      )}

    </div>
  );
}

export default Metric;