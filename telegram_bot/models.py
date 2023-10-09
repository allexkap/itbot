from django.db import models


class User(models.Model):
    telegram_id = models.IntegerField(primary_key=True)
    isu_id = models.IntegerField(null=True)

    def is_authenticated(self) -> bool:
        return self.isu_id is not None
