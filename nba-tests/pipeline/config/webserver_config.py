"""Local-only Airflow dashboard configuration.

This grants anonymous administration for an explicitly approved local
development-network dashboard. Do not reuse it for any public deployment.
"""

from flask_appbuilder.const import AUTH_DB

AUTH_TYPE = AUTH_DB
AUTH_ROLE_PUBLIC = "Admin"
