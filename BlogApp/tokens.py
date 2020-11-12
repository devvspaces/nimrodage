from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class EmailConfirmationToken(PasswordResetTokenGenerator):
	def _make_hash_value(self, email, timestamp):
		return(
		six.text_type(email.pk)+six.text_type(timestamp)+six.text_type(email.verified)
		)

email_confirm_token=EmailConfirmationToken()