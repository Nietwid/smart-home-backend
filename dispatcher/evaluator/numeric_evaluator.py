from rules.models import RuleCondition


def evaluate_numeric(current_value: float, cond: RuleCondition) -> bool:
    import operator

    ops = {
        ">": operator.gt,
        "<": operator.lt,
        ">=": operator.ge,
        "<=": operator.le,
    }

    op_str = cond.condition.get("operator")
    threshold = cond.condition.get("value")
    hysteresis = cond.condition.get("hysteresis", 0.0)
    last_triggered = cond.triggered

    if hysteresis == 0.0 or not last_triggered:
        is_currently_true = ops[op_str](current_value, threshold)
    elif op_str in [">", ">="]:
        is_currently_true = current_value > (threshold - hysteresis)
    else:
        is_currently_true = current_value < (threshold + hysteresis)

    if is_currently_true != last_triggered:
        cond.triggered = is_currently_true
        cond.save(update_fields=["triggered"])
        return is_currently_true
    return False
