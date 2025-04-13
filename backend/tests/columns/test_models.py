import pytest
from pydantic import ValidationError
from habit_tracker.columns.models import ColumnDetails, ColumnType, HabitValue  # replace with actual import


@pytest.mark.parametrize(
    "yaml_input,key,expected",
    [
        (
            {"column_type": "number", "display_name": "Sleep Hours"},
            "sleep",
            ColumnDetails(
                key="sleep", column_type=ColumnType.NUMBER, display_name="Sleep Hours", column_reference=None
            ),
        ),
        (
            {"column_type": "boolean", "display_name": "Worked Out", "column_reference": "A"},
            "worked_out",
            ColumnDetails(
                key="worked_out", column_type=ColumnType.BOOLEAN, display_name="Worked Out", column_reference="A"
            ),
        ),
    ],
    ids=["Without column reference", "With column reference"],
)
def test_from_yaml_valid(yaml_input: dict[str, str], key:str, expected: ColumnDetails):
    assert ColumnDetails.from_yaml(yaml_input, key) == expected


@pytest.mark.parametrize(
    "yaml_input",
    [
        {"display_name": "Sleep Hours"},
        {"column_type": "number"},
    ],
    ids = ["Missing column_type", "Missing display_name"],
)
def test_from_yaml_missing_keys_raises(yaml_input: dict[str, str]):
    with pytest.raises(KeyError):
        ColumnDetails.from_yaml(yaml_input, "dummy")

@pytest.mark.parametrize(
    "column_type,value,expected",
    [
        (ColumnType.NUMBER, 5, True),
        (ColumnType.NUMBER, 3.14, True),
        (ColumnType.NUMBER, True, False),
        (ColumnType.BOOLEAN, True, True),
        (ColumnType.BOOLEAN, False, True),
        (ColumnType.BOOLEAN, 1, False),
    ],
)
def test_check_value_type_matches(column_type: ColumnType, value: HabitValue, expected:bool):
    mock_column = ColumnDetails(key="test", column_type=column_type, display_name="Test")
    assert mock_column.check_value_type_matches(value) is expected
