from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models.abc import UUID7Model, CreatedUpdatedModel


class UserModel(UUID7Model, CreatedUpdatedModel, AbstractUser):

    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    # username_validator = UnicodeUsernameValidator()

    username = None
    first_name = None
    last_name = None
    email = None
    # is_staff = models.BooleanField(
    #     _("staff status"),
    #     default=False,
    #     help_text=_("Designates whether the user can log into this admin site."),
    # )
    # is_active = models.BooleanField(
    #     _("active"),
    #     default=True,
    #     help_text=_(
    #         "Designates whether this user should be treated as active. "
    #         "Unselect this instead of deleting accounts."
    #     ),
    # )
    date_joined = None

    # objects = UserManager()

    # [TODO] Разобраться с константами EMAIL_FIELD, USERNAME_FIELD, REQUIRED_FIELDS
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    # class Meta:
    #     verbose_name = _("user")
    #     verbose_name_plural = _("users")
    #     abstract = True

    def clean(self):
        # super().clean()
        # self.email = self.__class__.objects.normalize_email(self.email)
        raise NotImplementedError

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        raise NotImplementedError

    def get_short_name(self):
        """Return the short name for the user."""
        raise NotImplementedError

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        raise NotImplementedError
