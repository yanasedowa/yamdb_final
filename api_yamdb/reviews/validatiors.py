from django.forms import ValidationError


def validate_score(value):
    if not (0 < value < 11):
        raise ValidationError(
            'Используйте оценку от 1 до 10',
            params={'value': value})
