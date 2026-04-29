from django.db.models import QuerySet


from dispatcher.command_message.message import CommandMessage
from dispatcher.device.messages.enum import MessageCommand
from dispatcher.command_message.factory import command_message_factory
from dispatcher.evaluator.mapper_evaluator import MAPPER_EVALUATOR
from hardware.registry import HARDWARE_REGISTRY
from peripherals.models import Peripherals
from rules.models import Rule, RuleCondition


class RuleEngineService:

    @classmethod
    def get_event_request(
        cls,
        peripheral: Peripherals,
        event: MessageCommand,
    ) -> list[CommandMessage]:
        rules = cls.get_rules(peripheral, event)
        command_messages = []
        home_id = peripheral.device.home.id
        router_mac = peripheral.device.home.router.mac
        for rule in rules:
            if cls._check_conditions(rule.conditions.all()):
                for action in rule.actions.all().order_by("order"):
                    command_messages.append(
                        command_message_factory.get_commands_from_rule(
                            peripheral.device, home_id, router_mac, action
                        )
                    )
        return command_messages

    @classmethod
    def get_rules(
        cls, peripheral: Peripherals, event: MessageCommand
    ) -> QuerySet[Rule]:
        return Rule.objects.filter(
            device=peripheral.device,
            enabled=True,
            is_local=False,
            triggers__peripheral=peripheral,
            triggers__event=event,
        ).prefetch_related(
            "conditions", "conditions__peripheral", "actions", "actions__peripheral"
        )

    @classmethod
    def _check_conditions(cls, conditions: list[RuleCondition]) -> bool:
        if not conditions:
            return True

        for cond in conditions:
            hw_class = HARDWARE_REGISTRY.get(cond.peripheral.name)
            if not hw_class:
                raise Exception(f"Unsupported device type: {cond.peripheral.name}")

            attr_name = hw_class.event_to_attr.get(cond.event)
            if not attr_name:
                raise Exception(f"Unsupported event: {cond.event}")

            current_value = cond.peripheral.state.get(attr_name)
            if current_value is None:
                raise Exception(f"Attribute {attr_name} not found in payload")

            cond_type = cond.condition.get("type")

            evaluator = MAPPER_EVALUATOR.get(cond_type)

            if not evaluator:
                raise Exception(f"Unknown condition type: {cond_type}")

            is_met = evaluator(current_value, cond)
            if not is_met:
                return False
        return True
