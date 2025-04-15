import { Habit, useHabitContext } from "@/components/HabitProvider";
import { HabitCell } from "@/components/HabitTable/HabitCell";

type Props = {
  habit: Habit;
  dates: string[];
};

export function HabitRow({ habit, dates }: Props) {
  return (
    <tr>
      <td className="py-4 font-semibold text-xl text-center">{habit.name}</td>
      {dates.map(date => (
        <HabitCell key={date} habitId={habit.key} habitType={habit.type} date={date} />
      ))}
    </tr>
  );
}
