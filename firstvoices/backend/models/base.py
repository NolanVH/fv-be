import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from rules.contrib.models import RulesModel

from .constants import Visibility
from .managers import PermissionsManager


class BaseModel(RulesModel):
    """
    Base model for all FirstVoices Backend models, with standard fields and support for rules-based permissions.

    Date fields values are generated automatically, but user fields (created_by and last_modified_by) are required when
    creating new data.

    Access rules can be configured using a declaration in the Meta class, like this example:
    class Meta:
        rules_permissions = {
            "add": rules.is_staff,
            "view": rules.is_authenticated,
        }
    See the django-rules docs [https://github.com/dfunckt/django-rules#permissions-in-models] for more details.
    """

    class Meta:
        abstract = True

    # The permissions manager adds functionality to filter a queryset based on user permissions.
    objects = PermissionsManager()

    # from uid (and seemingly not uid:uid)
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )

    # from isTrashed
    is_trashed = models.BooleanField(default=False)

    # from dc:creator
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        related_name="created_%(app_label)s_%(class)s",
    )

    # from dc:created
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    # from dc:modified
    last_modified_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        related_name="modified_%(app_label)s_%(class)s",
    )

    # from dc:lastContributor
    last_modified = models.DateTimeField(auto_now=True, db_index=True)


class BaseSiteContentModel(BaseModel):
    """
    Base model for non-access-controlled site content data such as categories, that do not have their own
    visibility levels. Can also be used as a base for more specific types of site content base models.
    """

    class Meta:
        abstract = True

    site = models.ForeignKey(
        to="backend.Site", on_delete=models.CASCADE, related_name="%(class)s_set"
    )


class BaseControlledSiteContentModel(BaseSiteContentModel):
    """
    Base model for access-controlled site content models such as words, phrases, songs, and stories, that have their own
    visibility level setting.
    """

    class Meta:
        abstract = True

    visibility = models.IntegerField(
        choices=Visibility.choices, default=Visibility.TEAM
    )


# method to add last_modified and created fields if missing in the data, helpful for fixtures
@receiver(pre_save, sender="backend.PartOfSpeech")
@receiver(pre_save, sender="backend.appjson")
def pre_save_for_fixtures(sender, instance, **kwargs):
    if kwargs["raw"]:
        if not instance.created:
            instance.created = timezone.now()
        instance.last_modified = timezone.now()


class TruncatingCharField(models.CharField):
    """
    Custom field which auto truncates the value of a varchar field if it goes above a specific length.
    Also strips any whites spaces in the beginning or in the end before enforcing max length.
    Ref: https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.Field.get_prep_value
    """

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value:
            return value.strip()[: self.max_length]
        return value
