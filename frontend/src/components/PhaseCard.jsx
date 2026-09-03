function PhaseCard({
  number,
  title,
  subtitle,
  children,
}) {
  return (
    <section className="phase-card">

      <div className="phase-header">

        <div className="phase-number">
          {number}
        </div>

        <div className="phase-title">

          <span>
            PHASE {number}
          </span>

          <h2>
            {title}
          </h2>

          <p>
            {subtitle}
          </p>

        </div>

        <div className="completed">
          <span>✓</span>
          Completed
        </div>

      </div>

      <div className="phase-content">
        {children}
      </div>

    </section>
  );
}

export default PhaseCard;