from django.db import models


class User(models.Model):
    telegram_id = models.IntegerField(primary_key=True, db_index=True)
    isu_id = models.IntegerField(null=True, blank=True)
    workflow_state = models.CharField(max_length=32, null=True, blank=True)
    language = models.CharField(max_length=2, default='ru')
    access_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)
    id_token = models.TextField(null=True, blank=True)

    def is_authenticated(self) -> bool:
        return self.isu_id is not None

    def set_workflow_state(self, state: str) -> None:
        self.workflow_state = state
        self.save()

    def set_property(self, name: str, value: str) -> None:
        self.context_set.update_or_create(name=name, value=value)

    def get_property(self, name: str) -> str | None:
        try:
            return self.context_set.get(name=name).value
        except models.Context.DoesNotExist:
            return None

    def clear_properties(self) -> None:
        self.context_set.all().delete()


class Context(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    name = models.CharField(primary_key=True, max_length=32, db_index=True)
    value = models.CharField(max_length=32)
