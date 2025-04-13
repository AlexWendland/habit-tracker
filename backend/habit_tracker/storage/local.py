import datetime
from typing_extensions import override
from habit_tracker.columns.models import ColumnDetails, HabitValue
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
