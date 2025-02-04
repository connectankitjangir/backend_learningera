class SSCResultsRouter:
    """
    Direct SSC results queries to the SQLite database (data.db).
    """
    route_app_labels = {'ssc_results'}

    def db_for_read(self, model, **hints):
        """Direct read queries for SSC results to SQLite."""
        if model._meta.app_label in self.route_app_labels:
            return 'ssc_results_db'
        return None

    def db_for_write(self, model, **hints):
        """Prevent writing to SQLite."""
        if model._meta.app_label in self.route_app_labels:
            return None
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Disable migrations for SQLite."""
        if app_label in self.route_app_labels:
            return False
        return None
