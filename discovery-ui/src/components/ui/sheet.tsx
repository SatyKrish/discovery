import * as React from "react";
import { cn } from "@/lib/utils";

type SheetContextValue = { open: boolean; setOpen: (v: boolean) => void };
const SheetContext = React.createContext<SheetContextValue | undefined>(undefined);

interface SheetProps {
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  children: React.ReactNode;
}

function Sheet({ open: openProp, onOpenChange, children }: SheetProps) {
  const [openState, setOpenState] = React.useState(false);
  const open = openProp ?? openState;
  const setOpen = (v: boolean) => {
    if (openProp === undefined) setOpenState(v);
    onOpenChange?.(v);
  };
  return <SheetContext.Provider value={{ open, setOpen }}>{children}</SheetContext.Provider>;
}

interface SheetTriggerProps extends React.HTMLAttributes<HTMLDivElement> {
  asChild?: boolean;
}

const SheetTrigger = React.forwardRef<HTMLDivElement, SheetTriggerProps>(
  ({ asChild, children, ...props }, ref) => {
    const ctx = React.useContext(SheetContext);
    if (!ctx) return null;
    const trigger = (
      <div
        ref={ref}
        {...props}
        onClick={(e: React.MouseEvent<HTMLDivElement>) => {
          props.onClick?.(e);
          ctx.setOpen(!ctx.open);
        }}
      >
        {children}
      </div>
    );
    if (asChild && React.isValidElement(children)) {
      const child = children as React.ReactElement<{ onClick?: (e: React.MouseEvent<HTMLDivElement>) => void }>;
      return React.cloneElement(child, {
        onClick: (e: React.MouseEvent<HTMLDivElement>) => {
          child.props.onClick?.(e);
          ctx.setOpen(!ctx.open);
        },
      });
    }
    return trigger;
  }
);
SheetTrigger.displayName = "SheetTrigger";

interface SheetContentProps extends React.HTMLAttributes<HTMLDivElement> {
  side?: "left" | "right";
}

const SheetContent = React.forwardRef<HTMLDivElement, SheetContentProps>(
  ({ side = "right", className, children, ...props }, ref) => {
    const ctx = React.useContext(SheetContext);
    React.useEffect(() => {
      const handler = (e: KeyboardEvent) => {
        if (e.key === "Escape") ctx?.setOpen(false);
      };
      window.addEventListener("keydown", handler);
      return () => window.removeEventListener("keydown", handler);
    }, [ctx]);
    if (!ctx?.open) return null;
    return (
      <div className="fixed inset-0 z-50 flex">
        <div className="absolute inset-0 bg-black/40" onClick={() => ctx.setOpen(false)} />
        <div
          ref={ref}
          className={cn(
            "relative h-full w-3/4 max-w-sm bg-background shadow-lg",
            side === "left" ? "ml-0" : "ml-auto",
            className
          )}
          {...props}
        >
          {children}
        </div>
      </div>
    );
  }
);
SheetContent.displayName = "SheetContent";

const SheetHeader: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ className, ...props }) => (
  <div className={cn("px-4 py-2 border-b", className)} {...props} />
);

const SheetTitle: React.FC<React.HTMLAttributes<HTMLHeadingElement>> = ({ className, ...props }) => (
  <h3 className={cn("text-lg font-semibold", className)} {...props} />
);

export { Sheet, SheetTrigger, SheetContent, SheetHeader, SheetTitle };

