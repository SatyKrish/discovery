"use client";

import React from "react";
import { CheckCircle, AlertCircle, Clock, Loader } from "lucide-react";
import type { SubAgent } from "@/lib/types";

interface SubAgentIndicatorProps {
  subAgent: SubAgent;
  onClick: () => void;
}

export const SubAgentIndicator = React.memo<SubAgentIndicatorProps>(
  ({ subAgent, onClick }) => {
    const getStatusIcon = () => {
      switch (subAgent.status) {
        case "completed":
          return <CheckCircle className="w-4 h-4 text-green-600" />;
        case "error":
          return <AlertCircle className="w-4 h-4 text-red-600" />;
        case "pending":
          return <Loader className="w-4 h-4 animate-spin text-blue-600" />;
        default:
          return <Clock className="w-4 h-4 text-gray-600" />;
      }
    };

  return (
    <button
      onClick={onClick}
      className="flex items-start gap-2 md:gap-3 w-full p-3 md:p-4 bg-secondary border border-border rounded-lg text-left transition-colors hover:bg-secondary/80 focus:outline-none focus:ring-2 focus:ring-ring"
    >
      <div className="flex items-center justify-center w-7 h-7 md:w-8 md:h-8 rounded-full bg-primary/10 flex-shrink-0 mt-0.5">
        {getStatusIcon()}
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1 md:mb-2">
          <span className="font-medium text-sm text-foreground">{subAgent.subAgentName}</span>
        </div>
        <p className="text-xs md:text-sm text-muted-foreground line-clamp-2 m-0">
          {typeof subAgent.input === "string" ? subAgent.input : JSON.stringify(subAgent.input)}
        </p>
      </div>
    </button>
  );
  },
);

SubAgentIndicator.displayName = "SubAgentIndicator";
