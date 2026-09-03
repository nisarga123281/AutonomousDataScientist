import {
  Home,
  UploadCloud,
  BarChart3,
  Sparkles,
  ChartNoAxesCombined,
  BrainCircuit,
  Image,
  FileText,
  MessageCircle,
} from "lucide-react";

import "./Sidebar.css";

function Sidebar({ page, setPage }) {
  const menuItems = [
    {
      id: "dashboard",
      label: "Overview",
      icon: Home,
    },
    {
      id: "upload",
      label: "Upload Dataset",
      icon: UploadCloud,
    },
    {
      id: "profiling",
      label: "Profiling",
      icon: BarChart3,
    },
    {
      id: "cleaning",
      label: "Cleaning",
      icon: Sparkles,
    },
    {
      id: "eda",
      label: "EDA",
      icon: ChartNoAxesCombined,
    },
    {
      id: "modeling",
      label: "Modeling",
      icon: BrainCircuit,
    },
    {
      id: "visualizations",
      label: "Visualization",
      icon: Image,
    },
    {
      id: "ai-insights",
      label: "AI Insights",
      icon: Sparkles,
    },
    {
      id: "chat",
      label: "AI Chat",
      icon: MessageCircle,
    },
    {
      id: "report",
      label: "Report",
      icon: FileText,
    },
  ];

  const handleNavigation = (id) => {
    if (id === "dashboard") {
      setPage("dashboard");
      return;
    }

    if (id === "report") {
      setPage("phase7");
      return;
    }

    if (
      ["profiling", "cleaning", "eda", "modeling", "visualizations"].includes(
        id
      )
    ) {
      setPage(
        `phase${
          {
            profiling: 1,
            cleaning: 2,
            eda: 3,
            modeling: 4,
            visualizations: 5,
          }[id]
        }`
      );
      return;
    }

    if (id === "ai-insights") {
      setPage("phase6");
      return;
    }

    if (id === "chat") {
      setPage("chat");
      return;
    }

    if (id === "upload") {
      setPage("dashboard");
      return;
    }

    setPage("dashboard");
  };

  return (
    <aside className="sidebar">
      <nav className="sidebar-nav">
        {menuItems.map((item) => {
          const Icon = item.icon;

          const isActive =
            item.id === "dashboard"
              ? page === "dashboard"
              : item.id === "upload"
              ? page === "dashboard"
              : item.id === "profiling"
              ? page === "phase1"
              : item.id === "cleaning"
              ? page === "phase2"
              : item.id === "eda"
              ? page === "phase3"
              : item.id === "modeling"
              ? page === "phase4"
              : item.id === "visualizations"
              ? page === "phase5"
              : item.id === "ai-insights"
              ? page === "phase6"
              : item.id === "chat"
              ? page === "chat"
              : item.id === "report"
              ? page === "phase7"
              : false;

          return (
            <button
              key={item.id}
              className={isActive ? "sidebar-item active" : "sidebar-item"}
              onClick={() => handleNavigation(item.id)}
            >
              <Icon size={21} strokeWidth={1.7} />

              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>
    </aside>
  );
}

export default Sidebar;