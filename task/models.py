from django.db import models


class Category(models.Model):
    class Meta:
        db_table = 'task_categories'
        indexes = (
            models.Index(
                name='name',
                fields=[
                    'name',
                ],
            ),
        )

    name = models.CharField(unique=True, max_length=255)
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '{pk} - {name}'.format(
            pk=self.pk,
            name=self.name,
        )
