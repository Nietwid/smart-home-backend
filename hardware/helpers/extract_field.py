from typing import Any, List, Union


def extract_field(config: Union[dict, list], field: str) -> List[Any]:
    """
    Recursively searches a nested config (dicts and lists) and returns all values
    corresponding to the specified field name.

    Args:
        config (dict | list): The nested configuration to search.
        field (str): The field name to extract values for.

    Returns:
        List[Any]: A list of all values found for the given field.
    """
    results = []

    if isinstance(config, dict):
        for key, value in config.items():
            if key == field:
                results.append(value)
            else:
                results.extend(extract_field(value, field))
    elif isinstance(config, list):
        for item in config:
            results.extend(extract_field(item, field))

    return results
