import * as React from "react";

const Tabs: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children }) => <div>{children}</div>;
const TabsList: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children }) => <div>{children}</div>;
const TabsTrigger: React.FC<React.HTMLAttributes<HTMLButtonElement> & { asChild?: boolean }> = ({ children }) => <button>{children}</button>;
const TabsContent: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ children }) => <div>{children}</div>;

export { Tabs, TabsList, TabsTrigger, TabsContent };
