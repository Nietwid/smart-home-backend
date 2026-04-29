from dispatcher.evaluator.boolean_evaluator import evaluate_boolean
from dispatcher.evaluator.numeric_evaluator import evaluate_numeric

MAPPER_EVALUATOR = {"numeric": evaluate_numeric, "boolean": evaluate_boolean}
