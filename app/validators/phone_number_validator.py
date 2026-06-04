def validate_phone_number(value: str):

        if not value.isdigit():
            raise ValueError(
                "Phone number must contain only digits"
            )

        if len(value) != 10:
            raise ValueError(
                "Phone number must be exactly 10 digits"
            )

        return value