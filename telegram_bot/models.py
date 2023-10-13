from django.db import models


class User(models.Model):
    telegram_id = models.IntegerField(primary_key=True)
    isu_id = models.IntegerField(null=True)
    workflow_state = models.CharField(max_length=64, null=True)

    def is_authenticated(self) -> bool:
        return self.isu_id is not None


class WorkflowItem(models.Model):
    name = models.CharField(max_length=32)
    action = models.CharField(max_length=32)
    handler = models.CharField(max_length=32, null=True)
