from django.contrib import admin

from rules.models import Rule, RuleTrigger, RuleAction

# Register your models here.
admin.site.register(Rule)
admin.site.register(RuleTrigger)
admin.site.register(RuleAction)
