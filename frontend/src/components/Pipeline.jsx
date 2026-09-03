import React from "react";

const stages = [
  ["01", "Profiling", "◉"],
  ["02", "Cleaning", "✓"],
  ["03", "EDA", "⌁"],
  ["04", "Modeling", "◇"],
  ["05", "Visualization", "▥"],
  ["06", "AI Insights", "✦"],
  ["07", "Report", "▤"],
];
function Pipeline({ pipelineData }) {

  const completed =
    pipelineData?.workflow_status === "completed";

  return (
    <div className="workflow-card">

      {/* =========================
          PIPELINE HEADER
      ========================= */}
      <div className="workflow-top">

        <div>

          <div className="workflow-label">
            AUTONOMOUS EXECUTION
          </div>

          <h2>
            Pipeline Status
          </h2>

          <p>
            Seven specialized stages execute the complete
            data science workflow automatically.
          </p>

        </div>


        {/* STATUS */}
        <div
          className={`workflow-status ${
            completed ? "done" : ""
          }`}
        >

          <span></span>

          {completed
            ? "PIPELINE COMPLETED"
            : "READY TO ANALYZE"}

        </div>

      </div>


      {/* =========================
          PIPELINE TRACK
      ========================= */}
      <div className="pipeline-track">

        {stages.map((stage, index) => (

          <React.Fragment key={stage[0]}>

            {/* STAGE */}
            <div
              className={`pipeline-stage ${
                completed
                  ? "stage-completed"
                  : ""
              }`}
            >

              {/* ICON */}
              <div className="stage-circle">

                {completed
                  ? "✓"
                  : stage[2]}

              </div>


              {/* NUMBER */}
              <div className="stage-number">
                {stage[0]}
              </div>


              {/* NAME */}
              <div className="stage-name">
                {stage[1]}
              </div>


              {/* COMPLETION STATUS */}
              {completed && (
                <div className="stage-status">
                  COMPLETED
                </div>
              )}

            </div>


            {/* CONNECTOR */}
            {index < stages.length - 1 && (

              <div
                className={`pipeline-connector ${
                  completed
                    ? "connector-completed"
                    : ""
                }`}
              >
                <span></span>
              </div>

            )}

          </React.Fragment>

        ))}

      </div>

    </div>
  );
}

export default Pipeline;