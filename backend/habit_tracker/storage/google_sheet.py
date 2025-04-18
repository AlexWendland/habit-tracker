import datetime
from typing import override

import gspread

from habit_tracker.models import ColumnDetails, ColumnType, HabitValue
from habit_tracker.storage.base import StorageBase

CREDENTIAL_FILE = "drive-credentials.json"
HABIT_SHEET = "Habits"
HABIT_DATA_WORKSHEET = "data"
BASE_DATE = datetime.date(2025, 4, 2)

class GoogleSheetStorage(StorageBase):

    def __init__(self, habit_dictionary: dict[str, ColumnDetails], worksheet: gspread.Worksheet):
        self.habit_dictionary = habit_dictionary
        self._worksheet = worksheet

    @override
    def _get_single_value_by_day(self, habit_key: str, day: datetime.date) -> HabitValue:
        """
        Get the value of the cell for the given column name and date.

        When we call get we get back a cell range even if it is for a single cell. If this cell is blank cell.first()
        returns None.
        """
        cell_value: str | None = self._worksheet.get(self._get_cell(habit_key, day)).first()
        return self._parse_cell_value(cell_value, habit_key)

    @override
    def _set_single_value_by_day(self, habit_key: str, day: datetime.date, value: HabitValue) -> None:
        """
        Set the value of a habit for a specific day.
        """
        cell = self._get_cell(habit_key, day)
        column_type = self._get_column_type(habit_key)
        if column_type == ColumnType.NUMBER:
            self._worksheet.update_acell(cell, float(value))
        elif column_type == ColumnType.BOOLEAN:
            self._worksheet.update_acell(cell, "TRUE" if value else "FALSE")
        else:
            raise ValueError(f"Unknown column type: {column_type}")

    @override
    def _get_habit_values_between(self, habit_key: str, start_date: datetime.date, end_date: datetime.date) -> dict[datetime.date, HabitValue | None]:
        start_cell = self._get_cell(habit_key, start_date)
        end_cell = self._get_cell(habit_key, end_date)

        # Use .range() to get actual Cell objects, including empties
        cell_range = self._worksheet.range(f"{start_cell}:{end_cell}")

        result: dict[datetime.date, HabitValue | None] = {}
        current_date = start_date
        for cell in cell_range:
            value = cell.value if cell.value != "" else None
            result[current_date] = self._parse_cell_value(value, habit_key)
            current_date += datetime.timedelta(days=1)
    
        return result

    def _parse_cell_value(self, value:str | None, habit_key: str) -> HabitValue | None:
        column_type = self._get_column_type(habit_key)
        if column_type == ColumnType.NUMBER:
            return self._get_default_value(habit_key) if value is None else float(value)
        elif column_type == ColumnType.BOOLEAN:
            return self._get_default_value(habit_key) if value is None else value.lower() == "true"
        else:
            raise ValueError(f"Unknown column type: {column_details.column_type}")


    def _get_cell(self, column_name: str, date: datetime.date) -> str:
        """
        Get the cell address for the given column name and date.
        """
        column_char = self.habit_dictionary[column_name].column_reference
        column_index = _get_date_index(date)
        return f"{column_char}{column_index}"

def _get_date_index(date: datetime.date) -> int:
    """
    Get the index of the date in the sheet.
    """
    return (date - BASE_DATE).days + 2


def get_habit_worksheet() -> gspread.Worksheet:
    """
    Get the Google Sheet object.
    """
    gc = gspread.service_account(filename=CREDENTIAL_FILE)
    sh = gc.open(HABIT_SHEET)
    return sh.worksheet(HABIT_DATA_WORKSHEET)
