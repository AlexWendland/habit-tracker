from sheet.update_sheet import get_value, set_value
import datetime

CREDENTIAL_FILE = "drive-credentials.json"
HABIT_SHEET = "Habits"

def main():
    value = get_value("weight", datetime.date(2025,4,12))
    print(f"Value: {value}")
    set_value("weight", datetime.date(2025,4,12), 98)
    value = get_value("weight", datetime.date(2025,4,12))
    print(f"Value: {value}")

if __name__ == "__main__":
    main()
