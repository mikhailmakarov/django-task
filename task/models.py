from django.db import models
from django.utils import timezone


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

    @staticmethod
    def add_new_category(name, parent=None, children=[]):
        rows_processed = 1
        category, created = Category.objects.get_or_create(name=name)
        if not created and category.parent and category.parent != parent:
            category.try_rename_or_remove()
            category = Category(name=name)
        category.parent = parent
        category.save()

        children_names = []
        for child in children:
            rows_processed += Category.add_new_category(parent=category, **child)
            children_names.append(child['name'])

        # Remove parent category for child which not given as a child of a category
        for child in Category.objects.filter(parent=category):
            if child.name not in children_names:
                child.parent = None
                child.save()

        return rows_processed

    def try_rename_or_remove(self):
        old_name = self.name
        for x in range(3):
            try:
                self.name = '{date} Removed - {old_name}'.format(
                    date=timezone.now(),
                    old_name=old_name,
                )[:255]
                self.parent = None
                self.save()
                return
            except Exception:
                continue
        self.delete()

    def get_parents(self):
        result = []
        item = self
        while item.parent:
            item = item.parent
            result.append(item)
        return result

    def get_children(self):
        return Category.objects.filter(parent=self)

    def get_siblings(self):
        return Category.objects.filter(parent=self.parent).exclude(pk=self.pk)
