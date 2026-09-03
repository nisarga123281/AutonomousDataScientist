import { useState } from "react";
import "./App.css";

import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import Dashboard from "./components/Dashboard";
import AgentDetail from "./components/AgentDetail";
import Results from "./components/Results";
import Chat from "./components/Chat";

const stageAgents = {
  phase1: { id: "01", name: "Profiling", description: "Dataset structure and quality." },
  phase2: { id: "02", name: "Cleaning", description: "Data quality preparation." },
  phase3: { id: "03", name: "EDA", description: "Patterns, statistics and relationships." },
  phase4: { id: "04", name: "Modeling", description: "Predictive model evaluation." },
  phase5: { id: "05", name: "Visualization", description: "Interactive visual analysis." },
  phase6: { id: "06", name: "AI Insights", description: "Findings and interpretation." },
  phase7: { id: "07", name: "Report", description: "Complete analysis report." },
};

function App() {
  const [page, setPage] = useState("dashboard");
  const [pipelineData, setPipelineData] = useState(null);

  const backToOverview = () => {
    setPage("dashboard");
  };

  return (
    <div className="app">

      {/* Top Header */}
      <Header />

      <div className="app-layout">

        {/* Left Sidebar */}
        <Sidebar
          page={page}
          setPage={setPage}
        />

        {/* Main Content */}
        <main className="main-content">
          {page === "chat" && <Chat />}
          {/* Dashboard */}
          {page === "dashboard" && (
            <Dashboard
              setPage={setPage}
              pipelineData={pipelineData}
              setPipelineData={setPipelineData}
            />
          )}

          {page.startsWith("phase") && (
            <AgentDetail
              agent={stageAgents[page]}
              onBack={backToOverview}
              pipelineData={pipelineData}
            />
          )}

          {/* Results */}
          {page === "results" && (
            <Results
              pipelineData={pipelineData}
            />
          )}

        </main>
      </div>
    </div>
  );
}

export default App;