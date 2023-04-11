from django.db import models
from datetime import datetime


class RecordMixin(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    owner = models.ForeignKey('accounts.CustomUser',
                              on_delete=models.CASCADE,
                              related_name='%(app_label)s_%(class)s_related',
                              )

    class Meta:
        abstract = True

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        utcnow = datetime.utcnow()
        if not self.id:
            self.created_at = utcnow
        self.modified_at = utcnow

        return super().save(force_insert, force_update, using, update_fields)


class LikeIntermediaryMixin(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    class Meta:
        abstract = True
