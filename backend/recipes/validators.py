from django.core.validators import RegexValidator


class ColorValidator(RegexValidator):
    regex = '^#([-a-fA-F0-9_]$)'
    flags = 0
