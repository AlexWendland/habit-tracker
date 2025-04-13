from contextlib import contextmanager
import datetime
import fastapi
import os
from habit_tracker.columns.models import ColumnDetails, HabitValue
from habit_tracker.constants import PROD_ENV, COLUMN_FILE
from habit_tracker.columns.parsing import get_column_details
from habit_tracker.storage.local import LocalStorage, get_mock_local_storage
from habit_tracker.storage.google_sheet import GoogleSheetStorage, get_habit_worksheet
from math import isnan

app = fastapi.FastAPI()

def get_storage() -> LocalStorage | GoogleSheetStorage:
    global STORAGE
    if os.getenv(PROD_ENV):
        habits = get_column_details(COLUMN_FILE)
        sheet = get_habit_worksheet()
        return GoogleSheetStorage(habits, sheet)
    else:
        return get_mock_local_storage()

STORAGE: LocalStorage | GoogleSheetStorage = get_storage()

@app.get("/habits")
def get_habits() -> list[ColumnDetails]:
    global STORAGE
    return STORAGE.get_habits()

@app.get("/value")
def get_value(habit_key:str, day: datetime.date) -> HabitValue | None:
    value = STORAGE.get_habit_value_by_day(habit_key, day)
    return None if isnan(value) else value


@app.post("/value")
def set_value(habit_key:str, day: datetime.date, value: HabitValue):
    STORAGE.set_habit_value_by_day(habit_key, day, value)

