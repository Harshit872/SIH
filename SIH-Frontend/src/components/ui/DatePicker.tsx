import { useState, useRef, useEffect } from "react";
import { format, startOfDay } from "date-fns";
import { DayPicker, type DateRange } from "react-day-picker";
import "react-day-picker/dist/style.css";
import { Calendar as CalendarIcon } from "lucide-react";
import { Button } from "./button";

interface DatePickerProps {
  mode: "single" | "range";
  selected?: Date | DateRange | null;
  onSelect: (date: any) => void;
  placeholder?: string;
  error?: boolean;
}

export function DatePicker({ mode, selected, onSelect, placeholder, error }: DatePickerProps) {
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const getDisplayValue = () => {
    if (!selected) return placeholder || "Pick a date";
    if (mode === "single") {
      return format(selected as Date, "dd MMM yyyy");
    }
    const range = selected as DateRange;
    if (range.from) {
      if (range.to) {
        return `${format(range.from, "dd MMM yyyy")} - ${format(range.to, "dd MMM yyyy")}`;
      }
      return format(range.from, "dd MMM yyyy");
    }
    return placeholder || "Pick a date range";
  };

  const today = startOfDay(new Date());

  return (
    <div className="relative w-full" ref={containerRef}>
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className={`flex h-11 w-full items-center justify-start rounded-md border ${error ? 'border-destructive' : 'border-input'} bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2`}
      >
        <CalendarIcon size={16} className="mr-2 opacity-50" />
        <span className={selected ? "text-foreground" : "text-muted-foreground"}>
          {getDisplayValue()}
        </span>
      </button>

      {isOpen && (
        <div className="absolute top-full left-0 z-50 mt-1 rounded-md border border-border bg-popover text-popover-foreground shadow-md p-3 animate-in fade-in-0 zoom-in-95">
          <DayPicker
            mode={mode as any}
            selected={selected as any}
            onSelect={(day: any) => {
              onSelect(day);
              if (mode === "single") setIsOpen(false);
            }}
            disabled={{ before: today }}
            className="border-0"
          />
          {mode === "range" && (
            <div className="mt-3 flex justify-end">
              <Button type="button" size="sm" onClick={() => setIsOpen(false)}>
                Done
              </Button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
