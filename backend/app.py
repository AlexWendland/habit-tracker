import datetime
import os

import fastapi
from fastapi.middleware.cors import CORSMiddleware

from habit_tracker.columns.parsing import get_column_details
from habit_tracker.constants import COLUMN_FILE, PROD_ENV
from habit_tracker.models import ColumnDetails, HabitValue, HabitReturnValue
from habit_tracker.storage.google_sheet import GoogleSheetStorage, get_habit_worksheet
from habit_tracker.storage.local import LocalStorage, get_mock_local_storage

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/habits/{habit_key}/values/{day}")
def get_value(habit_key:str, day: datetime.date) -> HabitReturnValue:
    value = STORAGE.get_habit_value_by_day(habit_key, day)
    print(f"Value for {habit_key} on {day}: {value}")
    return HabitReturnValue(value = value)

@app.get("/habits/{habit_key}/values")
def get_values_between(habit_key:str, start_date: datetime.date, end_date: datetime.date) -> dict[datetime.date, HabitValue | None]:
    values = STORAGE.get_habit_values_between(habit_key, start_date, end_date)
    return values


@app.put("/habits/{habit_key}/values/{day}")
def set_value(habit_key:str, day: datetime.date, value: HabitReturnValue):
    print(f"Setting value for {habit_key} on {day}: {value.value} ({type(value.value)})")
    if value.value is None:
        raise fastapi.HTTPException(status_code=400, detail="Value cannot be None")
    STORAGE.set_habit_value_by_day(habit_key, day, value.value)

