from django.db import models


class User(models.Model):
    telegram_id = models.IntegerField(primary_key=True, db_index=True)
    isu_id = models.IntegerField(null=True)
    workflow_state = models.CharField(max_length=64, null=True)

    def is_authenticated(self) -> bool:
        return self.isu_id is not None

    def set_property(self, name, value) -> None:
        self.context_set.update_or_create(name=name, value=value)

    def get_property(self, name) -> str | None:
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
