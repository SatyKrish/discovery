import * as React from "react";

const DropdownMenu: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children }) => <div className="relative inline-block">{children}</div>;
const DropdownMenuTrigger: React.FC<React.HTMLAttributes<HTMLDivElement> & { asChild?: boolean }> = ({ children }) => <div>{children}</div>;
const DropdownMenuContent: React.FC<React.HTMLAttributes<HTMLDivElement> & { align?: string }> = ({ children }) => (
  <div className="absolute right-0 mt-2 w-56 rounded-md border bg-popover p-2 text-popover-foreground shadow-md">{children}</div>
);
const DropdownMenuItem: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children, ...props }) => (
  <div className="cursor-pointer select-none rounded-sm px-2 py-1.5 text-sm outline-none hover:bg-accent" {...props}>{children}</div>
);
const DropdownMenuLabel: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children }) => <div className="px-2 py-1.5 text-sm font-semibold">{children}</div>;
const DropdownMenuSeparator: React.FC<React.HTMLAttributes<HTMLDivElement>> = (props) => <div className="-mx-1 my-1 h-px bg-border" {...props} />;

export { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator };
