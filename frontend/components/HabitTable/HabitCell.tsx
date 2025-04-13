"use client";

import { useHabitContext } from "@/components/HabitProvider";
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

  return (
    <td className="px-2 py-1 text-center">
      {habitType === "number" ? (
        <NumberInput
          hideStepper
          value={value}
          onChange={handleChange}
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
