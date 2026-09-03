import {
  BrainCircuit,
  ChevronDown,
  CircleUserRound,
} from "lucide-react";

function Header() {
  return (
    <header className="app-header">

      {/* BRAND */}

      <div className="brand">

        <div className="brand-mark">
          <BrainCircuit size={42} strokeWidth={1.8} />
        </div>

        <div className="brand-text">

          <h1>
            Autonomous Data Scientist
          </h1>

          <p>
            AI-Powered End-to-End Data Analysis & Insights
          </p>

        </div>

      </div>


      {/* RIGHT SIDE */}

      <div className="header-right">

        <div className="system-status">

          <span className="status-dot"></span>

          <span>
            System Online
          </span>

        </div>


        <div className="ai-profile">

          <div className="profile-icon">
            <CircleUserRound
              size={27}
              strokeWidth={1.6}
            />
          </div>

          <div className="profile-text">

            <strong>
              Data Scientist AI
            </strong>

            <small>
              Autonomous Mode
            </small>

          </div>

          <ChevronDown
            size={16}
            className="profile-arrow"
          />

        </div>

      </div>

    </header>
  );
}

export default Header;