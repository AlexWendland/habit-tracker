import { createContext, useContext } from "react";

export const HabitContext = createContext(null);

export function useHabitContext() {
  const context = useContext(HabitContext);
  if (!context) throw new Error("Must be used within a HabitProvider");
  return context;
}
