from rest_framework.exceptions import ValidationError


class ValidateUsername:

    def validate_username(self, value):
        if '@' in value or '.' in value or ',' in value:
            raise ValidationError(
                "В username запрещены символы '@', '.' и ','!"
            )
        if value.lower() == 'me':
            raise ValidationError(
                "Username запрещено назначать равным 'me'!"
            )
        return value
