import rules
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _

from backend import predicates
from backend.models.base import BaseSiteContentModel
from backend.models.constants import CATEGORY_POS_MAX_TITLE_LENGTH


class Category(BaseSiteContentModel):
    """Model for Categories."""

    # Fields
    title = models.CharField(max_length=CATEGORY_POS_MAX_TITLE_LENGTH)
    description = models.TextField(blank=True)
    # i.e. A category may have a parent, but the parent category cannot have a parent itself. (i.e. no grandparents).
    # This is enforced in the clean method.
    parent = models.ForeignKey(
        "self", blank=True, null=True, on_delete=models.PROTECT, related_name="children"
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        unique_together = ("site", "title")
        rules_permissions = {
            "view": rules.always_allow,
            "add": predicates.is_superadmin,
            "change": predicates.is_superadmin,
            "delete": predicates.is_superadmin,
        }

    def __str__(self):
        return self.title

    def clean(self):
        self.is_cleaned = True
        # Enforce only one max level of nesting
        parent_category = self.parent
        if parent_category and parent_category.parent:
            raise ValidationError(
                _(
                    "A category may have a parent, but the parent category cannot have a parent itself. "
                    + "(i.e. no grandparents)"
                )
            )
        super().clean()

    def save(self, *args, **kwargs):
        if not hasattr(self, "is_cleaned"):
            self.is_cleaned = False
        if not self.is_cleaned:
            self.full_clean()
        super().save(*args, **kwargs)
