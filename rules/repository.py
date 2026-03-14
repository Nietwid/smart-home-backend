from django.db.models import QuerySet

from rules.models import Rule


class RuleRepository:

    @classmethod
    def get_rule(cls, rule_id: int) -> Rule:
        return Rule.objects.get(id=rule_id)

    @classmethod
    def get_local_ids(cls, device_mac: str) -> list[int]:
        return list(
            Rule.objects.filter(device__mac=device_mac, is_local=True).values_list(
                "id", flat=True
            )
        )
