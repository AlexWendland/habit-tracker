import { HabitProvider } from "@/components/HabitContext";
import { DashboardLayout } from "@/components/DashboardLayout";

export default function Home() {
  return (
    <HabitProvider>
      <DashboardLayout />
    </HabitProvider>
  );
}
