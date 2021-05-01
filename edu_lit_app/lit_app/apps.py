import json
import logging
import os

from django.apps import AppConfig

from edu_lit_app.settings import BASE_DIR

logger = logging.getLogger(__name__)

class LitAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lit_app'

    def ready(self):
        self.load_tests_from_json(BASE_DIR / 'sample_tests')

    def load_tests_from_json(self, path):
        from lit_app.models import Question, Test

        # DELETES ALL TESTS EVERY RUN
        logger.warning('Deleting every test record...')
        count = 0
        while test_record := Test.objects.first():
            count += 1
            test_record.delete()
        logger.warning(f'Deleted {count} test records')
        logger.info(f'Looking for new sample tests in {path}')
        for filename in os.listdir(path):
            filename = os.path.join(path, filename)
            if not filename.endswith('.json'):
                continue
            logger.info(f'Found sample test file {filename}')
            try:
                with open(filename, 'r') as f:
                    testcase = json.load(f)
            except json.JSONDecodeError as jde:
                logger.warning(f'Failed to parse {filename}: {jde.msg}')
                continue
            try:
                name = testcase['name']
                question = testcase['questions']
            except KeyError as ke:
                logger.warning(
                f'Failed to find mandatory field in sample test: {ke}'
                )
            if name := testcase.get('name'):
                if questions := testcase.get('questions'):
                    pass
                else:
                    logger.warning('Failed to find questions, skipping')
                    continue
            else:
                logger.warning('Failed to find name, skipping')
                continue

            test_record = Test(name=name)
            test_record.save()
            for question in questions:
                question_record = Question(
                    name=question['name'],
                    difficulty=question['difficulty'],
                    answer_blob=question['content'],
                    test_id=test_record.id
                )
                question_record.save()

        else:
            if not filename: # above loop didn't run, no sample tests found
                logger.warning(f'No tests found in {path}')
