import { Habit, useHabitContext } from "@/components/HabitProvider";
import { HabitCell } from "@/components/HabitTable/HabitCell";

type Props = {
  habit: Habit;
  dates: string[];
};

export function HabitRow({ habit, dates }: Props) {
  return (
    <tr>
      <td className="px-4 py-2 font-semibold">{habit.name}</td>
      {dates.map(date => (
        <HabitCell key={date} habitId={habit.key} habitType={habit.type} date={date} />
      ))}
    </tr>
  );
}
