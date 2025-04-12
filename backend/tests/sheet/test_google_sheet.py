import pytest
import datetime
from storage.google_sheet import _get_date_index


@pytest.mark.parametrize(
    "date, expected_index",
    [
        (datetime.date(2025, 4, 2), 2),
        (datetime.date(2025, 5, 1), 31),
    ],
    ids=["At base date", "Some date far away"],
)
def test_get_date_index(date: datetime.date, expected_index: int):
    assert _get_date_index(date) == expected_index
