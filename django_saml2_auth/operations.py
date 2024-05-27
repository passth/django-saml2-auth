from django.db.migrations.operations.base import Operation


class LockTimeout(Operation):
    reversible = True
    sql = "SET LOCAL lock_timeout = '%ds';"

    def __init__(self, timeout: int = 2):
        self.timeout = timeout

    def state_forwards(self, app_label, state):
        pass

    def database_forwards(
        self, app_label, schema_editor, from_state, to_state
    ):
        schema_editor.execute(self.sql % self.timeout)

    def database_backwards(
        self, app_label, schema_editor, from_state, to_state
    ):
        schema_editor.execute(self.sql % self.timeout)

    def describe(self):
        return f"Sets local lock timeout to {self.timeout}"
