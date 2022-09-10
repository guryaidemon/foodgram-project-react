from django.core.validators import RegexValidator


class ColorValidator(RegexValidator):
    regex = '^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    flags = 0
