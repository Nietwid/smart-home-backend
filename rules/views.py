from rest_framework.generics import CreateAPIView
from rules.models import Rule
from rules.serializers.rule import RuleSerializer

# Create your views here.


class CreateRule(CreateAPIView):
    model = Rule
    serializer_class = RuleSerializer
