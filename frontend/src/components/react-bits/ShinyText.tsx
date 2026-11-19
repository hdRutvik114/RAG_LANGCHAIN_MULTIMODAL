import React from "react";
import { cn } from "../../lib/utils";

interface ShinyTextProps {
  text: string;
  disabled?: boolean;
  speed?: number;
  className?: string;
}

export const ShinyText: React.FC<ShinyTextProps> = ({
  text,
  disabled = false,
  speed = 5,
  className = "",
}) => {
  const animationDuration = `${speed}s`;

  return (
    <span
      className={cn(
        "inline-block bg-clip-text text-transparent bg-gradient-to-r from-zinc-200 via-emerald-300 to-zinc-400 bg-[length:200%_auto]",
        !disabled && "animate-shimmer",
        className
      )}
      style={{
        animationDuration,
        backgroundImage:
          "linear-gradient(120deg, rgba(255, 255, 255, 0.4) 0%, rgba(52, 211, 153, 0.9) 50%, rgba(255, 255, 255, 0.4) 100%)",
        WebkitBackgroundClip: "text",
      }}
    >
      {text}
    </span>
  );
};

