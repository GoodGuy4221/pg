from django.db.models.fields import AutoFieldMixin, UUIDField

from uuid import uuid4


class UID4AutoField(AutoFieldMixin, UUIDField):
    def get_internal_type(self):
        return 'UID4AutoField'

    def rel_db_type(self, connection):
        return UUIDField().db_type(connection=connection)
