import * as React from "react";

const TooltipProvider: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children }) => <div>{children}</div>;
const Tooltip: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children }) => <div className="relative inline-block">{children}</div>;
const TooltipTrigger: React.FC<React.HTMLAttributes<HTMLDivElement> & { asChild?: boolean }> = ({ children }) => <div>{children}</div>;
const TooltipContent: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children }) => <div className="absolute z-50 rounded-md bg-popover p-2 text-xs text-popover-foreground shadow-md">{children}</div>;

export { TooltipProvider, Tooltip, TooltipTrigger, TooltipContent };
