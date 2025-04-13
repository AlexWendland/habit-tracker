from habit_tracker.columns.parsing import get_column_details
from habit_tracker.columns.models import ColumnDetails, ColumnType
from habit_tracker.constants import COLUMN_FILE

MOCK_FILE = "tests/columns/mock_columns.yaml"
MOCK_COLUMNS = {
    "test_number": ColumnDetails(
        key="test_number",
        column_reference="N",
        column_type=ColumnType.NUMBER,
        display_name="Number"
    ),
    "test_boolean": ColumnDetails(
        key="test_boolean",
        column_reference="B",
        column_type=ColumnType.BOOLEAN,
        display_name="Boolean"
    ),
    "test_no_reference": ColumnDetails(
        key="test_no_reference",
        column_type=ColumnType.NUMBER,
        display_name="No reference"
    ),
}

def test_mock_column_file_parses():
    assert get_column_details(MOCK_FILE) == MOCK_COLUMNS

def test_actual_colums_file_parses():
    assert len(get_column_details(COLUMN_FILE)) > 0

