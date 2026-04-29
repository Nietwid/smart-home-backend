from rules.models import RuleCondition


def evaluate_boolean(current_value: bool, cond: RuleCondition) -> bool:
    expected = cond.condition.get("value")
    is_currently_true = current_value == expected
    if is_currently_true != cond.triggered:
        cond.triggered = is_currently_true
        cond.save(update_fields=["triggered"])
        return is_currently_true

    return False
