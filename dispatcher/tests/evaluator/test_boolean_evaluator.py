import pytest
from model_bakery import baker
from rules.models import RuleCondition
from dispatcher.evaluator.boolean_evaluator import evaluate_boolean


@pytest.fixture
def boolean_cond(db):
    # Given
    return baker.make(
        RuleCondition, condition={"type": "boolean", "value": True}, triggered=False
    )


@pytest.mark.django_db
def test_evaluate_boolean_activation(boolean_cond):
    # When
    result = evaluate_boolean(True, boolean_cond)

    # Then
    assert result is True
    boolean_cond.refresh_from_db()
    assert boolean_cond.triggered is True


@pytest.mark.django_db
def test_evaluate_boolean_no_change(boolean_cond):
    # When
    result = evaluate_boolean(False, boolean_cond)

    # Then
    assert result is False
    boolean_cond.refresh_from_db()
    assert boolean_cond.triggered is False
