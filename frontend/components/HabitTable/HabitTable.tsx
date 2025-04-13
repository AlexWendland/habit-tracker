"use client";

import { useHabitContext } from "@/components/HabitProvider";
import { HabitHeader } from "@/components/HabitTable/HabitHeader";
import { HabitRow } from "@/components/HabitTable/HabitRow";

export function HabitTable() {
  const { habits, entries } = useHabitContext();

  const dates = Object.keys(entries[habits[0]?.id || ""] || {});

  return (
    <div className="overflow-x-auto border rounded-2xl shadow">
      <table className="table w-full text-sm">
        <thead>
          <HabitHeader dates={dates} />
        </thead>
        <tbody>
          {habits.map(habit => (
            <HabitRow key={habit.id} habit={habit} dates={dates} />
          ))}
        </tbody>
      </table>
    </div>
  );
}
