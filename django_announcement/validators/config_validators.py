from re import match
from typing import List

from django.core.checks import Error
from django.utils.module_loading import import_string

VALID_TIME_UNITS = ["second", "minute", "hour", "day"]


def validate_boolean_setting(value: bool, config_name: str) -> List[Error]:
    errors: List[Error] = []
    if not isinstance(value, bool):
        errors.append(
            Error(
                f"{config_name} is not a boolean.",
                hint=f"Ensure {config_name} is either True or False.",
                id=f"django_announcement.E001_{config_name}",
            )
        )
    return errors


def validate_list_fields(
    fields: List[str], config_name: str, allow_empty: bool = False
) -> List[Error]:
    errors = []
    if not isinstance(fields, list):
        errors.append(
            Error(
                f"{config_name} is not a list.",
                hint=f"Ensure {config_name} is a list of fields.",
                id=f"django_announcement.E002_{config_name}",
            )
        )
    elif not fields and not allow_empty:
        errors.append(
            Error(
                f"{config_name} is an empty list.",
                hint=f"Ensure {config_name} contains at least one field.",
                id=f"django_announcement.E003_{config_name}",
            )
        )
    else:
        invalid_fields = [field for field in fields if not isinstance(field, str)]
        if invalid_fields:
            errors.append(
                Error(
                    f"Invalid type(s) in {config_name}: {', '.join(map(str, invalid_fields))} are not strings.",
                    hint=f"Ensure all elements in {config_name} are strings.",
                    id=f"django_announcement.E004_{config_name}",
                )
            )

    return errors


def validate_throttle_rate(rate: str, setting_name: str) -> List[Error]:
    """
    Validates that a throttle rate is in the correct format: `{number}/{time_unit}`.

    Args:
        rate (str): The throttle rate to validate, e.g., "10/minute".
        setting_name (str): The name of the setting being validated (for error reporting).

    Returns:
        List[Error]: A list of errors if the rate is not valid, otherwise an empty list.
    """
    errors = []
    if not isinstance(rate, str) or "/" not in rate:
        errors.append(
            Error(
                f"'{setting_name}' must be an string in the format 'number/time_unit' (e.g., '10/minute').",
                id="django_announcement.E005",
            )
        )
        return errors

    # Split the rate into the number and the time unit
    parts = rate.split("/")
    if len(parts) != 2:
        errors.append(
            Error(
                f"'{setting_name}' is not in the correct format. Expected 'number/time_unit'.",
                id="django_announcement.E006",
            )
        )
        return errors

    number, time_unit = parts

    # Check if the number part is a valid integer
    if not number.isdigit():
        errors.append(
            Error(
                f"'{setting_name}' must start with a valid integer. Found: '{number}'.",
                id="django_announcement.E007",
            )
        )

    # Check if the time unit is valid
    if time_unit not in VALID_TIME_UNITS:
        errors.append(
            Error(
                f"'{setting_name}' has an invalid time unit: '{time_unit}'.",
                hint=f"Valid time units are: {', '.join(VALID_TIME_UNITS)}.",
                id="django_announcement.E008",
            )
        )

    return errors


def validate_optional_path_setting(
    setting_value: str, setting_name: str
) -> List[Error]:
    """Validate that the setting is a valid method or class path and can be
    imported.

    Args:
        setting_value (str): The value of the setting to validate, typically a method or class path.
        setting_name (str): The name of the setting being validated (for error reporting).

    Returns:
        List[Error]: A list of validation errors, or an empty list if valid.

    """
    errors: List[Error] = []

    if setting_value is None:
        # If the setting is None, we consider it optional and valid
        return errors

    if not isinstance(setting_value, str):
        errors.append(
            Error(
                f"The setting '{setting_name}' must be a valid string representing a method or class path.",
                hint=f"Ensure '{setting_name}' is set to a string (e.g., 'myapp.module.MyClass',"
                " myapp.module.my_method).",
                id=f"django_announcement.E009_{setting_name}",
            )
        )
        return errors

    # Attempt to import the class from the given path
    try:
        import_string(setting_value)
    except ImportError:
        errors.append(
            Error(
                f"Cannot import any method or class from the setting '{setting_name}'.",
                hint=f"Ensure the path '{setting_value}' is valid and importable.",
                id=f"django_announcement.E010_{setting_name}",
            )
        )

    return errors


def validate_optional_paths_setting(
    setting_value: List[str], setting_name: str
) -> List[Error]:
    """Validate that the setting value is a list of paths and ensure that they
    can be imported.

    Args:
        setting_value (List[str]): The setting value to validate, typically a list of method or class paths.
        setting_name (str): The name of the setting being validated (for error reporting).

    Returns:
        List[Error]: A list of validation errors, or an empty list if the setting is valid.

    """
    errors: List[Error] = []

    # If the setting is None, it's optional, so we consider it valid.
    if setting_value is None:
        return errors

    if not isinstance(setting_value, list):
        errors.append(
            Error(
                f"Invalid type for setting '{setting_name}'.",
                hint="The setting must be either a list of strings.",
                id=f"django_announcement.E011_{setting_name}",
            )
        )
        return errors

    # Validate each path in the list
    for path in setting_value:
        if not isinstance(path, str):
            errors.append(
                Error(
                    f"Invalid type for path in '{setting_name}'.",
                    hint="Each item in the list must be a valid string representing a path.",
                    id=f"django_announcement.E012_{setting_name}",
                )
            )
        else:
            # Attempt to import the method or path from the given path
            try:
                import_string(path)
            except ImportError:
                errors.append(
                    Error(
                        f"Cannot import the path from '{path}' in setting '{setting_name}'.",
                        hint=f"Ensure that '{path}' is a valid importable path.",
                        id=f"django_announcement.E013_{setting_name}",
                    )
                )

    return errors


def validate_upload_path_setting(path: str, setting_name: str) -> List[Error]:
    """Validate that the upload path is a proper string and follows a basic
    path structure.

    Args:
        path (str): The upload path to validate.
        setting_name (str): The name of the setting being validated.

    Returns:
        List[Error]: A list of validation errors if invalid, or an empty list if valid.

    """
    errors = []

    if not isinstance(path, str) or not path:
        errors.append(
            Error(
                f"{setting_name} must be a non-empty string.",
                hint="Ensure the upload path is provided as a non-empty string (e.g., 'uploads/announcements/').",
                id=f"django_announcement.E014_{setting_name}",
            )
        )

    return errors
