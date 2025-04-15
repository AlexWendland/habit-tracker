"use client";

import { useHabitContext } from "@/components/HabitContext";
import { Checkbox } from "@heroui/checkbox";
import { NumberInput } from "@heroui/number-input";
import { isToday } from "@/lib/dateUtils";

type Props = {
  habitId: string;
  habitType: "number" | "boolean";
  date: string;
};

export function HabitCell({ habitId, habitType, date }: Props) {
  const { entries, updateEntry } = useHabitContext();
  const value = entries[habitId]?.[date];

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = habitType === "number" ? Number(e.target.value) : e.target.checked;
    updateEntry({ habitId, date, value: newValue });
  };

  if (value == null || value === undefined) {
    return (
      <td 
        className={`px-2 py-1 ${
          isToday(date) ? "bg-secondary-100" : ""
        }`}
      >
      {habitType === "number" ? (
        <NumberInput
          hideStepper
          onChange={handleChange}
          aria-label={habitId}
          size="md"
          className="max-w-[5rem] mx-auto text-lg"
          radius="full"
        />
      ) : (
        <div className="flex justify-center">
          <Checkbox isSelected={false} size="lg" onValueChange={(val) => updateEntry({ habitId, date, value: val })} />
        </div>
      )}
      </td>
    );
  }

  return (
    <td 
      className={`px-2 py-1 ${
        isToday(date) ? "bg-secondary-100" : ""
      }`}
    >
      {habitType === "number" ? (
        <NumberInput
          hideStepper
          value={value}
          onChange={handleChange}
          aria-label={habitId}
          size="md"
          className="max-w-[5rem] mx-auto text-lg"
          radius="full"
        />
      ) : (
        <div className="flex justify-center">
          <Checkbox
            isSelected={Boolean(value)}
            size="lg"
            onValueChange={(val) => updateEntry({ habitId, date, value: val })}
          />
        </div>
      )}
    </td>
  );
}
