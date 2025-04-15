import abc
import datetime
from math import isnan

from habit_tracker.models import ColumnDetails, ColumnType, HabitValue


class StorageBase(abc.ABC):
    """
    Base class for storage backends.
    """

    habit_dictionary: dict[str, ColumnDetails]

    def get_habit_value_by_day(self, habit_key: str, day: datetime.date) -> HabitValue | None:
        """
        Get the value of a habit for a specific day.
        """
        if habit_key not in self.habit_dictionary:
            raise ValueError(f"Invalid habit key: {habit_key}")
        value = self._get_single_value_by_day(habit_key, day)
        if not self.habit_dictionary[habit_key].check_value_type_matches(value):
            raise ValueError(f"Value type mismatch for habit key: {habit_key}")
        # Handle NaN values for number types
        return None if isnan(value) else value

    def get_habit_values_between(self, habit_key: str, start_day: datetime.date, end_day: datetime.date) -> dict[datetime.date, HabitValue | None]:
        if habit_key not in self.habit_dictionary:
            raise ValueError(f"Invalid habit key: {habit_key}")
        if start_day > end_day:
            raise ValueError(f"Start date {start_day} cannot be after end date {end_day}")
        values = self._get_habit_values_between(habit_key, start_day, end_day)
        for date, value in values.items():
            if not self.habit_dictionary[habit_key].check_value_type_matches(value):
                raise ValueError(f"Value on day {date} type mismatch for habit key: {habit_key}")
        # Handle NaN values for number types
        return {date: (None if isnan(value) else value) for date, value in values.items()}

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

    def _get_column_type(self, habit_key: str) -> ColumnType:
        """
        Get the column type for a habit key.
        """
        if habit_key not in self.habit_dictionary:
            raise ValueError(f"Invalid habit key: {habit_key}")
        return self.habit_dictionary[habit_key].column_type

    def _get_default_value(self, habit_key: str) -> HabitValue:
        """
        Get the default value for a habit key.
        """
        column_type = self._get_column_type(habit_key)
        if column_type == ColumnType.NUMBER:
            return float("nan")
        elif column_type == ColumnType.BOOLEAN:
            return False
        else:
            raise ValueError(f"Unknown column type: {column_type}")


    @abc.abstractmethod
    def _get_habit_values_between(self, habit_key: str, start_date: datetime.date, end_date: datetime.date) -> dict[datetime.date, HabitValue | None]:
        """
        Gets the values of a habit between two dates (inclusive).
        """
        ...

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
