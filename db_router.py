class TestSeriesRouter:
    """
    A router to control all database operations for the `testseries` app to use `testseries_db`.
    """
    route_app_labels = {'testseries'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read `testseries` models go to `testseries_db`.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'testseries_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write `testseries` models go to `testseries_db`.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'testseries_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in `testseries` is involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the `testseries` app only appears in the `testseries_db` database.
        """
        if app_label in self.route_app_labels:
            return db == 'testseries_db'
        return None
