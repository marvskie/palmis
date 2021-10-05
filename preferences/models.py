from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class SystemPreferencesManager(models.Manager):

    def get_value(self, code: str):
        try:
            pref = self.get(code=code)
            if pref.val_type in [SystemPreference.TYPE_BOOLEAN, SystemPreference.TYPE_INT]:
                value = int(pref.value)
            else:
                value = pref.value
        except ObjectDoesNotExist:
            # fixtures not yet loaded
            return None
        return value


class SystemPreference(models.Model):
    TYPE_STR = 1
    TYPE_IMAGE = 2
    TYPE_BOOLEAN = 3
    TYPE_INT = 4
    TYPE_FLOAT = 5
    TYPE_TEXT = 6

    TYPE_CHOICES = (
        (TYPE_STR, 'String'),
        (TYPE_IMAGE, 'Image'),
        (TYPE_BOOLEAN, 'Boolean'),
        (TYPE_INT, 'Integer'),
        (TYPE_FLOAT, 'Float'),
        (TYPE_TEXT, 'Text')
    )
    objects = SystemPreferencesManager()

    name = models.CharField(max_length=64)
    code = models.CharField(max_length=20, unique=True)
    value = models.TextField()
    val_type = models.IntegerField(default=TYPE_STR, choices=TYPE_CHOICES, verbose_name='Value type')
    description = models.TextField(null=True, blank=True)
    remarks = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.code}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self._meta.fields:
            if field.name == 'value':
                field.help_text = self.remarks
                break
