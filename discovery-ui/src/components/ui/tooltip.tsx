import * as React from "react";
import { cn } from "@/lib/utils";

const TooltipProvider: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children }) => <div>{children}</div>;

type TooltipContextValue = { open: boolean; setOpen: (v: boolean) => void; controlled: boolean } | null;
const TooltipContext = React.createContext<TooltipContextValue>(null);

type TooltipProps = React.HTMLAttributes<HTMLDivElement> & { open?: boolean; defaultOpen?: boolean };
const Tooltip: React.FC<TooltipProps> = ({ children, open, defaultOpen = false, ...rest }) => {
	const [uncontrolledOpen, setUncontrolledOpen] = React.useState(defaultOpen);
	const isControlled = typeof open === "boolean";
	const value: TooltipContextValue = {
		open: isControlled ? (open as boolean) : uncontrolledOpen,
		setOpen: (v: boolean) => { if (!isControlled) setUncontrolledOpen(v); },
		controlled: isControlled,
	};
	return (
		<TooltipContext.Provider value={value}>
			<div className="relative inline-block" {...rest}>{children}</div>
		</TooltipContext.Provider>
	);
};

const TooltipTrigger: React.FC<React.HTMLAttributes<HTMLDivElement> & { asChild?: boolean }> = ({ children, ...rest }) => {
	const ctx = React.useContext(TooltipContext);
	return (
		<div
			onMouseEnter={() => ctx?.setOpen(true)}
			onMouseLeave={() => ctx?.setOpen(false)}
			onFocus={() => ctx?.setOpen(true)}
			onBlur={() => ctx?.setOpen(false)}
			{...rest}
		>
			{children}
		</div>
	);
};

type TooltipContentProps = React.HTMLAttributes<HTMLDivElement> & { side?: "top" | "bottom" | "left" | "right" };
const TooltipContent: React.FC<TooltipContentProps> = ({ children, side = "top", className, ...rest }) => {
	const ctx = React.useContext(TooltipContext);
	if (!ctx?.open) return null;
	const sideClasses: Record<string, string> = {
		top: "left-1/2 -translate-x-1/2 -top-2 -translate-y-full",
		bottom: "left-1/2 -translate-x-1/2 top-full mt-2",
		left: "right-full mr-2 top-1/2 -translate-y-1/2",
		right: "left-full ml-2 top-1/2 -translate-y-1/2",
	};
	return (
		<div
			className={cn(
				"absolute z-50 rounded-md bg-popover p-2 text-xs text-popover-foreground shadow-md",
				sideClasses[side],
				className
			)}
			role="tooltip"
			{...rest}
		>
			{children}
		</div>
	);
};

export { TooltipProvider, Tooltip, TooltipTrigger, TooltipContent };
