import datetime
import random
from typing import override

from habit_tracker.models import ColumnDetails, ColumnType, HabitValue
from habit_tracker.storage.base import StorageBase


class LocalStorage(StorageBase):

    def __init__(self, habit_dictionary: dict[str, ColumnDetails], start_values: dict[str, dict[datetime.date, HabitValue]]):
        self.habit_dictionary = habit_dictionary
        self._local_storage = start_values

    @override
    def _get_single_value_by_day(self, habit_key: str, day: datetime.date) -> HabitValue:
        return self._local_storage.get(habit_key, {}).get(day, self._get_default_value(habit_key))

    @override
    def _set_single_value_by_day(self, habit_key: str, day: datetime.date, value: HabitValue) -> None:
        self._local_storage.setdefault(habit_key, {})[day] = value

    @override
    def _get_habit_values_between(self, habit_key: str, start_date: datetime.date, end_date: datetime.date) -> dict[datetime.date, HabitValue]:
        """
        Gets the values of a habit between two dates (inclusive).
        """
        values = {}
        current_date = start_date
        while current_date <= end_date:
            values[current_date] = self._get_single_value_by_day(habit_key, current_date)
            current_date += datetime.timedelta(days=1)
        return values

def get_mock_local_storage() -> LocalStorage:
    """
    Create a mock local storage for testing.
    """
    habit_dictionary = {
        "weight": ColumnDetails(
            display_name="Weight",
            column_type=ColumnType.NUMBER,
            key="weight",
        ),
        "read": ColumnDetails(
            display_name="Read",
            column_type=ColumnType.BOOLEAN,
            key="read",
        )
    }
    start_values = {
        "weight": {datetime.date.today() - datetime.timedelta(days=i) : 80 + random.randint(-5, 5) for i in range(12)},
        "read": {datetime.date.today() - datetime.timedelta(days=i) : random.random() > 0.5 for i in range(12)},
    }
    return LocalStorage(habit_dictionary, start_values)
