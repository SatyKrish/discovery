import * as React from "react";

const Sheet: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children }) => <div>{children}</div>;
const SheetTrigger: React.FC<React.HTMLAttributes<HTMLDivElement> & { asChild?: boolean }> = ({ children }) => <div>{children}</div>;
const SheetContent: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children }) => <div>{children}</div>;
const SheetHeader: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children }) => <div>{children}</div>;
const SheetTitle: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children }) => <h3>{children}</h3>;

export { Sheet, SheetTrigger, SheetContent, SheetHeader, SheetTitle };
