import { Habit } from "@/types/habit";

export async function fetchHabits(): Promise<Habit[]> {
  const res = await fetch("http://localhost:8000/habits");
  if (!res.ok) throw new Error("Failed to fetch habit data");
  const json = await res.json();

  return json.map((habit: any) => ({
    key: habit.key,
    name: habit.display_name,
    type: habit.column_type,
  }));
}

export async function fetchHabitEntry(habitKey: string, date: string): Promise<number | boolean | null> {
  const url = `http://localhost:8000/habits/${encodeURIComponent(habitKey)}/values/${encodeURIComponent(date)}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch habit entry");
  const json = await res.json();
  return json.value ?? null;
}

export async function setHabitEntry(habitKey: string, date: string, value: number | boolean): Promise<void> {
  const url = `http://localhost:8000/habits/${encodeURIComponent(habitKey)}/values/${encodeURIComponent(date)}`;
  const res = await fetch(url, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ value }),
  });
  if (!res.ok) throw new Error("Failed to update habit entry");
}

export async function fetchHabitEntryBetween(
  habitKey: string,
  fromDate: string,
  toDate: string
): Promise<Record<string, number | boolean>> {
  const url = new URL(`http://localhost:8000/habits/${encodeURIComponent(habitKey)}/values`);
  url.searchParams.append("start_date", fromDate);
  url.searchParams.append("end_date", toDate);

  const res = await fetch(url.toString());
  if (!res.ok) throw new Error("Failed to fetch habit entries between dates");

  return await res.json(); // Expected to be a map of date strings to values
}
