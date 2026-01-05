from rest_framework.exceptions import ValidationError


def validate_language(value: str):
    if value and len(value) not in (2, 3):
        raise ValidationError(
            "Language code must be 2 or 3 characters long (e.g. 'en', 'fr', 'ka')."
        )


def validate_confidence(value: float):
    if value is not None and not (0.0 <= value <= 1.0):
        raise ValidationError("Confidence must be between 0.0 and 1.0.")


def validate_processing_time(value: float):
    if value is not None and value < 0:
        raise ValidationError("Processing time must be a positive number.")


def validate_tokens_used(value: int):
    if value is not None and value <= 0:
        raise ValidationError("Tokens used must be greater than zero.")


def validate_status_transition(instance, new_status):
    valid_transitions = {
        "pending": ["processing", "failed"],
        "processing": ["completed", "failed"],
        "completed": [],
        "failed": [],
    }

    if instance and new_status not in valid_transitions.get(instance.status, []):
        raise ValidationError(
            f"Invalid status transition from '{instance.status}' to '{new_status}'."
        )
