"use client";

import { useHabitContext } from "@/components/HabitContext";
import { Checkbox } from "@heroui/checkbox";
import { NumberInput } from "@heroui/number-input";

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
      <td className="px-2 py-1 text-center">
      {habitType === "number" ? (
        <NumberInput
          hideStepper
          onChange={handleChange}
          aria-label={habitId}
          size="sm"
          className="max-w-[4rem] mx-auto"
          radius="full"
        />
      ) : (
        <div className="flex justify-center">
          <Checkbox isSelected={false} onValueChange={(val) => updateEntry({ habitId, date, value: val })} />
        </div>
      )}
      </td>
    );
  }

  return (
    <td className="px-2 py-1 text-center">
      {habitType === "number" ? (
        <NumberInput
          hideStepper
          value={value}
          onChange={handleChange}
          aria-label={habitId}
          size="sm"
          className="max-w-[4rem] mx-auto"
          radius="full"
        />
      ) : (
        <div className="flex justify-center">
          <Checkbox
            isSelected={Boolean(value)}
            onValueChange={(val) => updateEntry({ habitId, date, value: val })}
          />
        </div>
      )}
    </td>
  );
}
