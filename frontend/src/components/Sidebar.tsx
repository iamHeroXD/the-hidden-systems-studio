"use client";

import React from "react";
import {
  LayoutDashboard,
  Compass,
  Clapperboard,
  FileText,
  Film,
  Sparkles,
  Mic,
  ShieldCheck,
  FolderKanban,
  BarChart3,
  CalendarClock,
  Settings,
  Tv
} from "lucide-react";

export type NavItem =
  | "overview"
  | "topics"
  | "production"
  | "script"
  | "storyboard"
  | "animation"
  | "voice"
  | "quality"
  | "library"
  | "analytics"
  | "automation"
  | "settings";

interface SidebarProps {
  currentTab: NavItem;
  onSelectTab: (tab: NavItem) => void;
  productionStatus?: string;
  schedulerEnabled?: boolean;
}

export const Sidebar: React.FC<SidebarProps> = ({
  currentTab,
  onSelectTab,
  productionStatus = "idle",
  schedulerEnabled = true
}) => {
  const navItems: { id: NavItem; label: string; icon: React.ReactNode; badge?: string }[] = [
    { id: "overview", label: "Overview", icon: <LayoutDashboard size={18} /> },
    { id: "topics", label: "Topic Intelligence", icon: <Compass size={18} />, badge: "20" },
    { id: "production", label: "Production Studio", icon: <Clapperboard size={18} />, badge: productionStatus === "running" ? "LIVE" : undefined },
    { id: "script", label: "Script Editor", icon: <FileText size={18} /> },
    { id: "storyboard", label: "Storyboard", icon: <Film size={18} />, badge: "40" },
    { id: "animation", label: "Animation Preview", icon: <Sparkles size={18} /> },
    { id: "voice", label: "Voice Studio", icon: <Mic size={18} /> },
    { id: "quality", label: "Quality Control", icon: <ShieldCheck size={18} /> },
    { id: "library", label: "Video Library", icon: <FolderKanban size={18} /> },
    { id: "analytics", label: "Analytics", icon: <BarChart3 size={18} /> },
    { id: "automation", label: "Automation", icon: <CalendarClock size={18} />, badge: schedulerEnabled ? "06:00" : "OFF" },
    { id: "settings", label: "Settings", icon: <Settings size={18} /> },
  ];

  return (
    <aside className="w-64 bg-studio-900 border-r border-studio-800 flex flex-col h-screen select-none">
      {/* Brand Header */}
      <div className="p-5 border-b border-studio-800">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-studio-amber to-amber-600 flex items-center justify-center shadow-lg shadow-studio-amber/10">
            <Tv size={18} className="text-studio-950 font-bold" />
          </div>
          <div>
            <h1 className="font-semibold text-sm tracking-wider text-studio-chalk uppercase">
              The Hidden Systems
            </h1>
            <p className="text-[11px] font-mono text-studio-amber tracking-tight">
              STUDIO ENGINE v1.0
            </p>
          </div>
        </div>
      </div>

      {/* Navigation List */}
      <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
        {navItems.map((item) => {
          const isActive = currentTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onSelectTab(item.id)}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-md text-xs font-medium transition-all ${
                isActive
                  ? "bg-studio-800 text-studio-chalk border-l-2 border-studio-amber shadow-sm"
                  : "text-studio-muted hover:text-studio-chalk hover:bg-studio-850"
              }`}
            >
              <div className="flex items-center gap-3">
                <span className={isActive ? "text-studio-amber" : "text-studio-muted"}>
                  {item.icon}
                </span>
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span
                  className={`px-1.5 py-0.5 text-[10px] font-mono rounded ${
                    item.badge === "LIVE"
                      ? "bg-studio-crimson/20 text-studio-crimson animate-pulse"
                      : "bg-studio-800 text-studio-muted border border-studio-700/50"
                  }`}
                >
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Channel Focus Tagline */}
      <div className="p-4 border-t border-studio-800 bg-studio-950/40">
        <div className="flex items-center justify-between text-[11px] font-mono text-studio-muted mb-1">
          <span>DAILY CADENCE</span>
          <span className="text-studio-emerald flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-studio-emerald animate-ping" />
            STANDALONE
          </span>
        </div>
        <p className="text-[10px] text-zinc-500 line-clamp-2">
          Autonomous 10–15 min documentary pipeline. Operates without open IDE.
        </p>
      </div>
    </aside>
  );
};
