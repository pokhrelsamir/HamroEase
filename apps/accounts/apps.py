from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"

    # Python import path
    name = "apps.accounts"

    # Django app label
    label = "accounts"

    verbose_name = "Accounts"