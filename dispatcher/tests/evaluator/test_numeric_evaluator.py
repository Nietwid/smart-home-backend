import pytest
from model_bakery import baker
from rules.models import RuleCondition
from dispatcher.evaluator.numeric_evaluator import evaluate_numeric


@pytest.fixture
def numeric_cond(db):
    # Given
    return baker.make(
        RuleCondition,
        condition={
            "type": "numeric",
            "operator": ">",
            "value": 25.0,
            "hysteresis": 2.0,
        },
        triggered=False,
    )


@pytest.mark.django_db
def test_evaluate_numeric_activation(numeric_cond):
    # When
    result = evaluate_numeric(26.0, numeric_cond)

    # Then
    assert result is True
    numeric_cond.refresh_from_db()
    assert numeric_cond.triggered is True


@pytest.mark.django_db
def test_evaluate_numeric_hysteresis_prevent_flicker(numeric_cond):
    # Given
    numeric_cond.triggered = True
    numeric_cond.save()

    # When
    result = evaluate_numeric(24.0, numeric_cond)

    # Then
    assert result is False
    numeric_cond.refresh_from_db()
    assert numeric_cond.triggered is True


@pytest.mark.django_db
def test_evaluate_numeric_deactivation_below_hysteresis(numeric_cond):
    # Given
    numeric_cond.triggered = True
    numeric_cond.save()

    # When
    result = evaluate_numeric(22.0, numeric_cond)

    # Then
    assert result is False
    numeric_cond.refresh_from_db()
    assert numeric_cond.triggered is False


@pytest.mark.django_db
def test_evaluate_numeric_calls_save_only_on_change(mocker, numeric_cond):
    # Given
    spy_save = mocker.spy(numeric_cond, "save")

    # When
    evaluate_numeric(20.0, numeric_cond)

    # Then
    assert spy_save.call_count == 0
    assert numeric_cond.triggered is False
