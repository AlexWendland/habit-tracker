import pytest
from pydantic import ValidationError
from your_module import ColumnDetails, ColumnType  # replace with actual import


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
def test_from_yaml_valid(yaml_input, key, expected):
    result = ColumnDetails.from_yaml(yaml_input, key)
    assert result == expected


@pytest.mark.parametrize(
    "yaml_input",
    [
        {"column_type": "number", "display_name": "Sleep Hours"},  # Missing key
        {"key": "sleep", "display_name": "Sleep Hours"},  # Missing column_type
        {"key": "sleep", "column_type": "number"},  # Missing display_name
    ],
)
def test_from_yaml_missing_keys_raises(yaml_input):
    with pytest.raises(KeyError):
        ColumnDetails.from_yaml(yaml_input, yaml_input.get("key", "dummy"))


# --- Tests for check_value_type_matches ---


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
def test_check_value_type_matches(column_type, value, expected):
    col = ColumnDetails(key="test", column_type=column_type, display_name="Test")
    assert col.check_value_type_matches(value) is expected
