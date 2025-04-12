import abc
import datetime

from habit_tracker.columns.models import ColumnDetails, HabitValue


class StorageBase(abc.ABC):
    """
    Base class for storage backends.
    """

    habit_dictionary: dict[str, ColumnDetails]

    def get_habit_value_by_day(self, habit_key: str, day: datetime.date) -> HabitValue:
        """
        Get the value of a habit for a specific day.
        """
        if habit_key not in self.habit_dictionary:
            raise ValueError(f"Invalid habit key: {habit_key}")
        value = self._get_single_value_by_day(habit_key, day)
        if not self.habit_dictionary[habit_key].check_value_type_matches(value):
            raise ValueError(f"Value type mismatch for habit key: {habit_key}")
        return value

    def set_habit_value_by_day(self, habit_key: str, day: datetime.date, value: HabitValue) -> None:
        """
        Set the value of a habit for a specific day.
        """
        if habit_key not in self.habit_dictionary:
            raise ValueError(f"Invalid habit key: {habit_key}")
        if not self.habit_dictionary[habit_key].check_value_type_matches(value):
            raise ValueError(f"Value type mismatch for habit key: {habit_key}")
        self._set_single_value_by_day(habit_key, day, value)

    def get_habits(self) -> list[ColumnDetails]:
        """
        Get the dictionary of habits.
        """
        return list(self.habit_dictionary.values())

    @abc.abstractmethod
    def _get_single_value_by_day(self, habit_key: str, day: datetime.date) -> HabitValue:
        """
        Get the value of a habit for a specific day.
        """
        ...

    @abc.abstractmethod
    def _set_single_value_by_day(self, habit_key: str, day: datetime.date, value: HabitValue) -> None:
        """
        Set the value of a habit for a specific day.
        """
        ...
