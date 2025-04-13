"use client";

import { HabitTable } from "@/components/HabitTable/HabitTable";
import { useHabitContext } from "@/components/HabitProvider";

export function DashboardLayout() {
  const { habits, entries } = useHabitContext();

  // Get the unique dates based on the first habit's entries
  const dates = Object.keys(entries[habits[0]?.id || ""] || {});

  return (
    <div className="p-6 space-y-6">
      {/* Header Section */}
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-semibold">Habit Dashboard</h1>
        <p className="text-lg text-gray-500">
          Track your habits daily — record your weight, reading, exercise, and more!
        </p>
      </div>

      {/* Habit Table Section */}
      <div className="overflow-x-auto shadow-lg rounded-lg p-4">
        <HabitTable />
      </div>

      {/* Add any extra sections here if needed */}
      {/* For example, for graphs or stats */}
    </div>
  );
}
