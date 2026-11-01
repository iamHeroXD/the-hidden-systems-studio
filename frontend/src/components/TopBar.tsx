"use client";

import React from "react";
import { Cpu, HardDrive, Play, DollarSign, Activity } from "lucide-react";

interface TopBarProps {
  telemetry?: {
    cpu_percent: number;
    ram_used_gb: number;
    ram_total_gb: number;
    ram_percent: number;
    disk_free_gb: number;
    gpu_name: string;
  };
  costs?: {
    daily_cost_usd: number;
    daily_limit_usd: number;
  };
  productionStatus?: string;
  onTriggerRun?: () => void;
  isTriggering?: boolean;
}

export const TopBar: React.FC<TopBarProps> = ({
  telemetry,
  costs,
  productionStatus = "idle",
  onTriggerRun,
  isTriggering = false
}) => {
  return (
    <header className="h-14 bg-studio-900 border-b border-studio-800 px-6 flex items-center justify-between select-none">
      {/* Left: Production Status Indicator */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <span
            className={`w-2 h-2 rounded-full ${
              productionStatus === "running"
                ? "bg-studio-amber animate-pulse"
                : productionStatus === "awaiting_approval"
                ? "bg-studio-teal"
                : productionStatus === "completed"
                ? "bg-studio-emerald"
                : "bg-zinc-600"
            }`}
          />
          <span className="text-xs font-mono font-medium text-studio-chalk uppercase">
            STUDIO: {productionStatus.replace("_", " ")}
          </span>
        </div>
      </div>

      {/* Right: Telemetry, Cost Guard, and Quick Trigger Button */}
      <div className="flex items-center gap-6">
        {/* Hardware Status */}
        {telemetry && (
          <div className="hidden lg:flex items-center gap-4 text-[11px] font-mono text-studio-muted border-r border-studio-800 pr-5">
            <div className="flex items-center gap-1.5" title="CPU Utilization">
              <Cpu size={14} className="text-zinc-400" />
              <span>{telemetry.cpu_percent.toFixed(0)}%</span>
            </div>
            <div className="flex items-center gap-1.5" title="RAM Utilization">
              <Activity size={14} className="text-zinc-400" />
              <span>
                {telemetry.ram_used_gb} / {telemetry.ram_total_gb} GB
              </span>
            </div>
            <div className="flex items-center gap-1.5" title="Storage Free">
              <HardDrive size={14} className="text-zinc-400" />
              <span>{telemetry.disk_free_gb} GB FREE</span>
            </div>
          </div>
        )}

        {/* Cost Guard */}
        {costs && (
          <div className="flex items-center gap-1.5 text-[11px] font-mono text-studio-muted border-r border-studio-800 pr-5">
            <DollarSign size={14} className="text-studio-amber" />
            <span>
              ${costs.daily_cost_usd.toFixed(2)} / ${costs.daily_limit_usd.toFixed(2)}
            </span>
          </div>
        )}

        {/* Trigger Automation Button */}
        <button
          onClick={onTriggerRun}
          disabled={isTriggering || productionStatus === "running"}
          className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-xs font-medium tracking-wide transition-all ${
            productionStatus === "running"
              ? "bg-studio-800 text-studio-muted cursor-not-allowed border border-studio-700/50"
              : "bg-studio-amber text-studio-950 hover:bg-amber-400 shadow-sm font-semibold active:scale-95"
          }`}
        >
          <Play size={13} fill="currentColor" />
          <span>{isTriggering ? "STARTING..." : "RUN PRODUCTION NOW"}</span>
        </button>
      </div>
    </header>
  );
};
