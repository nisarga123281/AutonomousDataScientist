
function OverviewCards({ data }) {
  if (!data) {
    return null;
  }

  const missingValues = Object.values(
    data.missing_values || {}
  ).reduce((total, value) => total + Number(value), 0);

  const cards = [
    {
      title: "Total Rows",
      value: data.rows ?? 0,
      icon: "▦",
    },
    {
      title: "Total Columns",
      value: data.columns ?? 0,
      icon: "▥",
    },
    {
      title: "Numerical",
      value: data.numerical_columns?.length ?? 0,
      icon: "∑",
    },
    {
      title: "Categorical",
      value: data.categorical_columns?.length ?? 0,
      icon: "Aa",
    },
    {
      title: "Duplicates",
      value: data.duplicate_rows ?? 0,
      icon: "⧉",
    },
    {
      title: "Missing Values",
      value: missingValues,
      icon: "!",
    },
  ];

  return (
    <section className="overview-section">

      <div className="section-heading">
        <div>
          <span className="section-label">
            DATASET OVERVIEW
          </span>

          <h2>Dataset Health</h2>

          <p>
            Key metrics automatically extracted from your
            uploaded dataset.
          </p>
        </div>
      </div>

      <div className="overview-grid">

        {cards.map((card) => (
          <div
            className="metric-card"
            key={card.title}
          >

            <div className="metric-icon">
              {card.icon}
            </div>

            <div className="metric-content">

              <span>
                {card.title}
              </span>

              <strong>
                {card.value}
              </strong>

            </div>

          </div>
        ))}

      </div>

    </section>
  );
}

export default OverviewCards;
