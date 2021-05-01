from django.apps import AppConfig

from edu_lit_app.settings import BASE_DIR

class LitAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lit_app'

    def ready(self):
        self.load_tests_from_json(BASE_DIR / 'sample_tests')

    def load_tests_from_json(self, path):
        for f[2] in (for _, _, filenames in next(os.walk(path)]):
