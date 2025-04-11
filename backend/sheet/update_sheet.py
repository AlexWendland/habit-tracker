from typing_extensions import Self
import gspread
import functools
import enum
import pydantic
import yaml
import datetime

CREDENTIAL_FILE = "drive-credentials.json"
HABIT_SHEET = "Habits"
HABIT_DATA_WORKSHEET = "data"
COLUMN_YAML = "columns.yaml"
BASE_DATE = datetime.date(2025, 4, 2)

cell_type = float | bool

class ColumnType(enum.Enum):
    NUMBER = enum.auto()
    BOOLEAN = enum.auto()

class ColumnDetails(pydantic.BaseModel):
    sheet_column: str
    column_type: ColumnType

    @classmethod
    def from_yaml(cls, details: dict[str,str]) -> Self:
        """
        Create a ColumnDetails object from YAML details.
        """
        return cls(sheet_column=details["sheet_column"], column_type=ColumnType[details["column_type"].upper()])


def get_value(column_name: str, date: datetime.date) -> cell_type:
    """
    Get the value of the cell for the given column name and date.

    When we call get we get back a cell range even if it is for a single cell. If this cell is blank cell.first()
    returns None.
    """
    worksheet = _get_habit_data_work_sheet()
    cell = worksheet.get(_get_cell(column_name, date))
    column_details = _read_columns()[column_name]
    if column_details.column_type == ColumnType.NUMBER:
        return 0.0 if cell.first() is None else float(cell.first())
    elif column_details.column_type == ColumnType.BOOLEAN:
        return False if cell.first() is None else cell.first().lower() == "true"
    else:
        raise ValueError(f"Unknown column type: {column_details.column_type}")

def set_value(column_name: str, date: datetime.date, value: cell_type) -> None:
    """
    Set the value of the cell for the given column name and date.
    """
    worksheet = _get_habit_data_work_sheet()
    cell = _get_cell(column_name, date)
    column_details = _read_columns()[column_name]
    if column_details.column_type == ColumnType.NUMBER:
        if not isinstance(value, (int, float)):
            raise ValueError(f"Value must be a number for column {column_name}")
        worksheet.update_acell(cell, float(value))
    elif column_details.column_type == ColumnType.BOOLEAN:
        if not isinstance(value, bool):
            raise ValueError(f"Value must be a boolean for column {column_name}")
        worksheet.update_acell(cell, "TRUE" if value else "")
    else:
        raise ValueError(f"Unknown column type: {column_details.column_type}")

def _get_cell(column_name: str, date: datetime.date) -> str:
    """
    Get the cell address for the given column name and date.
    """
    column_char = _read_columns()[column_name].sheet_column
    column_index = _get_date_index(date)
    return f"{column_char}{column_index}"

def _get_date_index(date: datetime.date) -> int:
    """
    Get the index of the date in the sheet.
    """
    return (date - BASE_DATE).days + 2

@functools.lru_cache(maxsize=1)
def _read_columns() -> dict[str, ColumnDetails]:
    """
    Read the column details from the YAML file.
    """
    with open(COLUMN_YAML, "r") as f:
        columns = yaml.safe_load(f)
        return {col: ColumnDetails.from_yaml(details) for col, details in columns.items()}

@functools.lru_cache(maxsize=1)
def _get_habit_data_work_sheet() -> gspread.Worksheet:
    """
    Get the Google Sheet object.
    """
    gc = gspread.service_account(filename=CREDENTIAL_FILE)
    sh = gc.open(HABIT_SHEET)
    return sh.worksheet(HABIT_DATA_WORKSHEET)

