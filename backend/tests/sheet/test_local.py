import datetime
import pytest
from math import isnan

from habit_tracker.models import ColumnDetails, ColumnType, HabitValue
from habit_tracker.storage.local import LocalStorage

MOCK_DATE = datetime.date(2023, 10, 1)

@pytest.fixture(scope="function")
def mock_date() -> datetime.date:
    return MOCK_DATE

@pytest.fixture(scope="function")
def mock_storage(mock_date:datetime.date) -> LocalStorage:
    habits = {
        "water": ColumnDetails(
            display_name="Water Intake",
            column_type=ColumnType.NUMBER,
            key="water",
        ),
        "exercise": ColumnDetails(
            display_name="Exercise",
            column_type=ColumnType.BOOLEAN,
            key="exercise",
        )
    }
    values = {
        "water": {mock_date: 2.5},
        "exercise": {mock_date: True}
    }
    return LocalStorage(habits, values)

def is_equal_with_nan_check(value1: HabitValue, value2: HabitValue) -> bool:
    return value1 == value2 or (isnan(value1) and isnan(value2))

@pytest.mark.parametrize(
    "column, day, expected",
    [
        ("water", MOCK_DATE, 2.5),
        ("exercise", MOCK_DATE, True),
        ("water", datetime.date(2023, 10, 2), None),
        ("exercise", datetime.date(2023, 10, 2), False),
    ]
)
def test_get_habit_value_by_day(mock_storage: LocalStorage, column:str, day: datetime.date, expected: HabitValue):
    assert is_equal_with_nan_check(mock_storage.get_habit_value_by_day(column, day), expected)

def test_get_habits(mock_storage:LocalStorage):
    assert mock_storage.get_habits() == [
        ColumnDetails(
            display_name="Water Intake",
            column_type=ColumnType.NUMBER,
            key="water",
        ),
        ColumnDetails(
            display_name="Exercise",
            column_type=ColumnType.BOOLEAN,
            key="exercise",
        )
    ]

@pytest.mark.parametrize(
    "column, day, expected",
    [
        ("water", datetime.date(2023,10,2), 2.3),
        ("exercise", datetime.date(2024,10,2), True),
        ("water", MOCK_DATE, 1),
        ("exercise", MOCK_DATE, False),
    ]
)
def test_set_habit_value_by_day_valid(mock_storage: LocalStorage, column:str, day:datetime.date, expected: HabitValue):
    mock_storage.set_habit_value_by_day(column, day, expected)
    assert mock_storage.get_habit_value_by_day(column, day) == expected

def test_invalid_key(mock_storage:LocalStorage, mock_date: datetime.date):
    with pytest.raises(ValueError):
        _ = mock_storage.get_habit_value_by_day("sleep", mock_date)
    with pytest.raises(ValueError):
        mock_storage.set_habit_value_by_day("sleep", mock_date, 8.0)
    with pytest.raises(ValueError):
        mock_storage._get_column_type("sleep")

@pytest.mark.parametrize(
    "column, bad_value",
    [
        ("water", False),
        ("exercise", 2.4),
    ]
)
def test_set_habit_value_by_day_invalid_type(mock_storage: LocalStorage, column: str, bad_value: float):
    with pytest.raises(ValueError):
        mock_storage.set_habit_value_by_day(column, datetime.date(2023, 10, 2), bad_value)


def test_get_column_type(mock_storage:LocalStorage):
    assert mock_storage._get_column_type("water") == ColumnType.NUMBER
    assert mock_storage._get_column_type("exercise") == ColumnType.BOOLEAN

@pytest.mark.parametrize(
    "column, expected_value",
    [
        ("water", float("nan")),
        ("exercise", False),
    ]
    )
def test_get_default_value(column: str, expected_value: HabitValue, mock_storage: LocalStorage):
    assert is_equal_with_nan_check(mock_storage._get_default_value(column), expected_value)

@pytest.mark.parametrize(
    "habit_value, expected",
    [
        ("water", {MOCK_DATE: 2.5, MOCK_DATE+datetime.timedelta(days=1): None}),
        ("exercise", {MOCK_DATE: True, MOCK_DATE + datetime.timedelta(days=1): False})
    ]
)
def test_get_habit_values_between(mock_storage: LocalStorage, habit_value: str, expected: dict[datetime.date, HabitValue | None]):
    assert mock_storage.get_habit_values_between(habit_value, MOCK_DATE, datetime.date(2023, 10, 2)) == expected
