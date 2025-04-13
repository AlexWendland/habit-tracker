"use client";

import { createContext, useContext, useState } from "react";

// Move these into a types file later.
type Habit = {
  id: string;
  name: string;
  type: "number" | "boolean";
};

type Entries = {
  [habitId: string]: {
    [date: string]: number | boolean;
  };
};

// Work out how this goes into habit context later.
const HabitContext = createContext<{
  habits: Habit[];
  entries: Entries;
  updateEntry: (args: { habitId: string; date: string; value: number | boolean }) => void;
} | null>(null);

export const useHabitContext = () => {
  const context = useContext(HabitContext);
  if (!context) throw new Error("useHabitContext must be used within a HabitProvider");
  return context;
};

// Hardcoded mock data
const initialHabits: Habit[] = [
  { id: "weight", name: "Weight", type: "number" },
  { id: "read", name: "Read", type: "boolean" },
];

const get14DayWindow = (): string[] => {
  const today = new Date();
  return [...Array(14)].map((_, i) => {
    const date = new Date(today);
    date.setDate(today.getDate() - (12 - i));
    return date.toISOString().split("T")[0];
  });
};

const initialEntries: Entries = (() => {
  const dates = get14DayWindow();
  return {
    weight: Object.fromEntries(dates.map(d => [d, Math.round(70 + Math.random() * 5)])),
    read: Object.fromEntries(dates.map(d => [d, Math.random() > 0.5])),
  };
})();

export function HabitProvider({ children }: { children: React.ReactNode }) {
  const [habits] = useState<Habit[]>(initialHabits);
  const [entries, setEntries] = useState<Entries>(initialEntries);

  const updateEntry = ({ habitId, date, value }: { habitId: string; date: string; value: number | boolean }) => {
    setEntries(prev => ({
      ...prev,
      [habitId]: {
        ...prev[habitId],
        [date]: value,
      },
    }));
  };

  return (
    <HabitContext.Provider value={{ habits, entries, updateEntry }}>
      {children}
    </HabitContext.Provider>
  );
}
