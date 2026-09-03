import { getReportUrl } from "../services/api";

function Report({ data }) {

    if (!data) return null;

    return (
        <section className="result-card report-card">

            <div className="phase-header">

                <div className="phase-number">
                    07
                </div>

                <div>
                    <span>PHASE 07</span>
                    <h2>Final Report</h2>
                    <p>Complete automated data science report</p>
                </div>

                <div className="completed">
                    ✓ Completed
                </div>

            </div>

            <div className="report-content">

                <div className="report-icon">
                    ▤
                </div>

                <div className="report-text">

                    <h3>
                        AutoDS Final Report
                    </h3>

                    <p>
                        Your dataset analysis has been processed
                        through profiling, cleaning, EDA, modeling,
                        visualization and AI insights.
                    </p>

                    <a
                        href={getReportUrl(data.report_file)}
                        target="_blank"
                        rel="noreferrer"
                        className="report-button"
                    >
                        View Final Report
                        <span>→</span>
                    </a>

                </div>

            </div>

        </section>
    );
}

export default Report;