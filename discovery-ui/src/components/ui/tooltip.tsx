import * as React from "react";
import { cn } from "@/lib/utils";

const TooltipProvider: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children }) => <>{children}</>;

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

const TooltipTrigger: React.FC<React.HTMLAttributes<HTMLElement> & { asChild?: boolean }> = ({ children, asChild, className, ...rest }) => {
	const ctx = React.useContext(TooltipContext);

	const handleMouseEnter = () => ctx?.setOpen(true);
	const handleMouseLeave = () => ctx?.setOpen(false);
	const handleFocus = () => ctx?.setOpen(true);
	const handleBlur = () => ctx?.setOpen(false);

	// If asChild, clone the child element and merge our event handlers
		if (asChild && React.isValidElement(children)) {
			const child = children as React.ReactElement<Record<string, unknown>>;
			const merge = <E extends React.SyntheticEvent>(userHandler?: (e: E) => void, ourHandler?: (e: E) => void) => (e: E) => {
				try { userHandler?.(e); } finally { ourHandler?.(e); }
			};
		const mergedProps = {
			...rest,
			className: cn(child.props.className as string | undefined, className),
				onMouseEnter: merge<React.MouseEvent>(child.props.onMouseEnter as ((e: React.MouseEvent) => void) | undefined, handleMouseEnter as (e: React.MouseEvent) => void),
				onMouseLeave: merge<React.MouseEvent>(child.props.onMouseLeave as ((e: React.MouseEvent) => void) | undefined, handleMouseLeave as (e: React.MouseEvent) => void),
				onFocus: merge<React.FocusEvent>(child.props.onFocus as ((e: React.FocusEvent) => void) | undefined, handleFocus as (e: React.FocusEvent) => void),
				onBlur: merge<React.FocusEvent>(child.props.onBlur as ((e: React.FocusEvent) => void) | undefined, handleBlur as (e: React.FocusEvent) => void),
		};
		return React.cloneElement(child, mergedProps);
	}

	// Default: wrap in a span, don't leak asChild to the DOM
	return (
		<span
			className={className}
			onMouseEnter={handleMouseEnter}
			onMouseLeave={handleMouseLeave}
			onFocus={handleFocus}
			onBlur={handleBlur}
			{...rest}
		>
			{children}
		</span>
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
