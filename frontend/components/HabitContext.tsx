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
import { fetchHabits, fetchHabitEntry, setHabitEntry } from "@/lib/habitsApi";
import { get14DayWindow } from "@/lib/dateUtils";

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
  await Promise.all(
    habits.map(async (habit) => {
      result[habit.key] = {};
      await Promise.all(
        dates.map(async (date) => {
          const value = await fetchHabitEntry(habit.key, date);
          result[habit.key][date] = value;
        })
      );
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

        const dates = get14DayWindow();
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
