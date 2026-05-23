import pytest
from django.apps import apps
from django.db import connection

@pytest.fixture(scope="session", autouse=True)
def setup_unmanaged_models(django_db_setup, django_db_blocker):
    """
    managed=False로 설정된 모델들의 테이블을 테스트 데이터베이스에 강제로 생성합니다.
    """
    unmanaged_models = [m for m in apps.get_models() if not m._meta.managed]
    with django_db_blocker.unblock():
        with connection.schema_editor() as editor:
            for model in unmanaged_models:
                try:
                    editor.create_model(model)
                except Exception:
                    pass # 테이블이 이미 존재하거나 에러가 날 경우 무시
        yield
        with connection.schema_editor() as editor:
            for model in unmanaged_models:
                try:
                    editor.delete_model(model)
                except Exception:
                    pass
