from .settings import *

# Выполнять задачи Celery сразу, синхронно (только для тестов)
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
