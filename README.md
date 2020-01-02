# Healthchecks SMTP Login Backend

This is a modified version of the healthchecks.io backends.py file with the ability to
login using a SMTP account.

Get Healthchecks.io here: https://github.com/healthchecks/healthchecks

## Installation Instructions

Replace the default EmailBackend in "hc/accounts/backends.py" with this updated class.

Add these imports to the backends file:
```python
from uuid import uuid4
from smtplib import SMTP
from django.conf import settings
```

The following options need to be added to "hc/settings.py":
```text
AUTH_SMTP_HOST     - Hostname of SMTP server (string)
AUTH_SMTP_PORT     - Port for SMTP server (int)
AUTH_SMTP_CREATE   - Create a user for this SMTP email if login is valid and no DB user exists (bool)
AUTH_SMTP_DOMAINS  - Valid domains for auto-generated user accounts. Only valid if AUTH_SMTP_CREATE is True (bool)
AUTH_SMTP_STARTTLS - Use STARTTLS for SMTP (bool)
```
