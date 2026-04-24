import pytest


@pytest.fixture(scope="session")
def celery_config():
    return {
        "task_always_eager": True,
        "task_eager_propagates": True,
    }


@pytest.fixture
def mock_notifier(mocker):
    return mocker.patch("consumers.tasks.notifier.notify")
