export type Habit = {
  key: string;
  name: string;
  type: "number" | "boolean";
};

export type Entries = {
  [habitId: string]: {
    [date: string]: number | boolean | null;
  };
};

