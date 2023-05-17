from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_name_me(name):
    """Валидатор модели user, поле username."""
    if name.lower() == "me":
        raise ValidationError('Имя не должно быть me')

    validator = RegexValidator(
        regex=r'^[\w.@+-]+$',
        message='Некорректный slug.'
    )
    validator(name)
