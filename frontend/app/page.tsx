import { HabitProvider } from "@/components/HabitProvider";
import { DashboardLayout } from "@/components/DashboardLayout";

export default function Home() {
  return (
    <HabitProvider>
      <DashboardLayout />
    </HabitProvider>
  );
}
