// context/HabitContext.tsx
"use client";

import {
  createContext,
  useContext,
  useEffect,
  useState,
  ReactNode,
} from "react";
import { Habit, Entries } from "@/types/habit";
import { fetchHabits, fetchHabitEntryBetween, setHabitEntry } from "@/lib/habitsApi";
import { getWindow } from "@/lib/dateUtils";

type HabitContextType = {
  habits: Habit[];
  entries: Entries;
  updateEntry: (args: {
    habitId: string;
    date: string;
    value: number | boolean;
  }) => void;
};

const HabitContext = createContext<HabitContextType | null>(null);

export const useHabitContext = () => {
  const context = useContext(HabitContext);
  if (!context) {
    throw new Error("useHabitContext must be used within a HabitProvider");
  }
  return context;
};

async function getInitialEntries(habits: Habit[], dates: string[]): Promise<Entries> {
  const result: Entries = {};
  const start_date = dates[0];
  const end_date = dates[dates.length - 1];
  await Promise.all(
    habits.map(async (habit) => {
      result[habit.key] = await fetchHabitEntryBetween(habit.key, start_date, end_date)
    })
  );
  return result;
}

export function HabitProvider({ children }: { children: ReactNode }) {
  const [habits, setHabits] = useState<Habit[]>([]);
  const [entries, setEntries] = useState<Entries>({});
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const habits = await fetchHabits();
        setHabits(habits);

        const dates = getWindow();
        const entries = await getInitialEntries(habits, dates);
        setEntries(entries);
        console.log("Entries:",entries);
      } catch (err) {
        console.error("Error loading habit data:", err);
      } finally {
        setIsLoading(false);
      }
    };
    load();
  }, []);

  const updateEntry = ({
    habitId,
    date,
    value,
  }: {
    habitId: string;
    date: string;
    value: number | boolean;
  }) => {
    setEntries((prev) => ({
      ...prev,
      [habitId]: {
        ...prev[habitId],
        [date]: value,
      },
    }));
    setHabitEntry(habitId, date, value).catch((err) => {
      console.error("Failed to update habit entry:", err);
    });
  };

  if (isLoading) return <div>Loading habits...</div>;

  return (
    <HabitContext.Provider value={{ habits, entries, updateEntry }}>
      {children}
    </HabitContext.Provider>
  );
}
