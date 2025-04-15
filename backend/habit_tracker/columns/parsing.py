import functools

import yaml

from habit_tracker.models import ColumnDetails


@functools.lru_cache(maxsize=1)
def get_column_details(yaml_file: str) -> dict[str, ColumnDetails]:
    """
    This function reads the YAML file and returns a dictionary of ColumnDetails objects keying from their key.
    """
    with open(yaml_file) as f:
        columns: dict[str, dict[str, str]] = yaml.safe_load(f)
        return {key: ColumnDetails.from_yaml(details, key) for key, details in columns.items()}
