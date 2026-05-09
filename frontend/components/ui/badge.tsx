import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium transition-colors",
  {
    variants: {
      variant: {
        default: "border-transparent bg-zinc-900 text-white dark:bg-zinc-50 dark:text-zinc-900",
        secondary: "border-transparent bg-zinc-100 text-zinc-700 dark:bg-zinc-800 dark:text-zinc-300",
        success: "border-transparent bg-emerald-50 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-400",
        warning: "border-transparent bg-amber-50 text-amber-700 dark:bg-amber-900/20 dark:text-amber-400",
        destructive: "border-transparent bg-red-50 text-red-700 dark:bg-red-900/20 dark:text-red-400",
        outline: "border-zinc-200 text-zinc-700 dark:border-zinc-700 dark:text-zinc-300",
      },
    },
    defaultVariants: { variant: "default" },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />
}

export { Badge, badgeVariants }
