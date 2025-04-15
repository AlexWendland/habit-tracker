from habit_tracker.columns.parsing import get_column_details
from habit_tracker.constants import COLUMN_FILE
from habit_tracker.storage.google_sheet import GoogleSheetStorage, get_habit_worksheet
import datetime

if __name__ == '__main__':
    habits = get_column_details(COLUMN_FILE)
    sheet = get_habit_worksheet()
    storage = GoogleSheetStorage(habits, sheet)
    data = storage.get_habit_values_between("weight", datetime.date(2025, 4, 10), datetime.date(2025, 4, 15))
    print(data)
