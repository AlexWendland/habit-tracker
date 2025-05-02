export function getWindow(): string[] {
  const today = new Date();
  return Array.from({ length: 9 }, (_, i) => {
    const date = new Date(today);
    date.setDate(today.getDate() - (7 - i));
    return date.toISOString().split("T")[0];
  });
}

export function convertDateToDayOfWeek(date: string): string {
  const dayOfWeek = new Date(date).toLocaleString("en-US", { weekday: "short" });
  return dayOfWeek.charAt(0).toUpperCase() + dayOfWeek.slice(1);
}

export function getShortDate(date: string): string {
  const options: Intl.DateTimeFormatOptions = { month: "2-digit", day: "2-digit" };
  return new Date(date).toLocaleDateString("en-US", options);
}

export function isToday(date: string): boolean {
  const today = new Date().toISOString().split("T")[0];
  return date === today;
}
