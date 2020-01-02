"""
SMTP Authentication for Healthchecks.io

Replace the default EmailBackend in "hc/accounts/backends.py" with this updated class.

The following options need to be added to "hc/settings.py":

AUTH_SMTP_HOST     - Hostname of SMTP server (string)
AUTH_SMTP_PORT     - Port for SMTP server (int)
AUTH_SMTP_CREATE   - Create a user for this SMTP email if login is valid and no DB user exists (bool)
AUTH_SMTP_DOMAINS  - Valid domains for auto-generated user accounts. Only valid if AUTH_SMTP_CREATE is True (bool)
AUTH_SMTP_STARTTLS - Use STARTTLS for SMTP (bool)
"""

"""
Add these imports to the top of the file.
"""
from uuid import uuid4
from smtplib import SMTP
from django.conf import settings
"""
End Imports
"""

class EmailBackend(BasicBackend):
    def authenticate_smtp(self, username, password):
        try:
            with SMTP(host=settings.AUTH_SMTP_HOST, port=settings.AUTH_SMTP_PORT) as s:
                if settings.AUTH_SMTP_STARTTLS:
                    s.starttls()
                s.login(username, password)
                s.noop()
                s.close()
        except Exception:
            return None
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            user = None
        if user is None and settings.AUTH_SMTP_CREATE:
            d = username.split("@")
            if len(d) == 2 and len(d[1]) > 0:
                if d[1].lower() not in settings.AUTH_SMTP_DOMAINS:
                    return None
            user = User.objects.create_user(
                username, email=username, password=str(uuid4())
            )
        return user

    def authenticate(self, request=None, username=None, password=None):
        user = self.authenticate_smtp(username, password)
        if user is not None:
            return user
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
