function StatusCard() {
  return (
    <div className="status-card">

      <div className="status-icon">
        ✓
      </div>

      <div className="status-content">

        <span>
          WORKFLOW STATUS
        </span>

        <h3>
          Pipeline Completed Successfully
        </h3>

        <p>
          AutoDS has completed all automated data
          science stages for your dataset.
        </p>

      </div>

      <div className="completed-badge">
        ✓ Completed
      </div>

    </div>
  );
}

export default StatusCard;