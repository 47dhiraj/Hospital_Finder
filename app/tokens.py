from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Combine user pk, timestamp, and is_active to generate a unique token
        return str(user.pk) + str(timestamp) + str(user.is_active)

account_activation_token = TokenGenerator()
