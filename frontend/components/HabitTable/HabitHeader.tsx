type Props = {
  dates: string[];
};

export function HabitHeader({ dates }: Props) {
  return (
    <tr className="">
      <th className="text-left px-4 py-2 font-medium">Habit</th>
      {dates.map(date => (
        <th key={date} className="text-center px-4 py-2 font-medium">
          {date}
        </th>
      ))}
    </tr>
  );
}
