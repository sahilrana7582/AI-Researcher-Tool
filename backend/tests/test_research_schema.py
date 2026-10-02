import pytest
from pydantic import ValidationError

from app.schemas.research import ResearchRequest


@pytest.mark.parametrize("query", ["", "   ", "x" * 5001])
def test_invalid_query_is_rejected(query):
    with pytest.raises(ValidationError):
        ResearchRequest(query=query)


def test_query_at_max_length_is_accepted():
    assert len(ResearchRequest(query="x" * 5000).query) == 5000


def test_query_whitespace_is_stripped():
    assert ResearchRequest(query="  what is RAG?  ").query == "what is RAG?"
