import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_missing_api_key_fails_fast(monkeypatch):
    monkeypatch.delenv("LLM_API_KEY")

    with pytest.raises(ValidationError, match="llm_api_key"):
        Settings(_env_file=None)


def test_api_key_is_masked_in_repr():
    settings = Settings(_env_file=None)

    assert "test-key" not in repr(settings)
    assert settings.llm_api_key.get_secret_value() == "test-key"


def test_unknown_env_file_keys_are_ignored(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("POSTGRES_URL=postgresql://localhost/db\n")

    Settings(_env_file=env_file)
