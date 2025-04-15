import { convertDateToDayOfWeek, getShortDate, isToday } from "@/lib/dateUtils";

type Props = {
  dates: string[];
};

export function HabitHeader({ dates }: Props) {
  return (
    <tr>
      <th className="text-center px-4 py-4 font-medium text-lg">Habit</th>
      {dates.map((date) => {

        return (
          <th
            key={date}
            className={`text-center px-2 py-3 ${
              isToday(date) ? "bg-secondary-100" : ""
            }`}
          >
            <div className="text-xl font-bold leading-tight">
              {convertDateToDayOfWeek(date)}
            </div>
            <div className="text-sm text-default-400">
              {getShortDate(date)}
            </div>
          </th>
        );
      })}
    </tr>
  );
}
