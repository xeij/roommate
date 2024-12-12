import pytest
from app.browse import search_user_by_name_or_building
import app.browse

def test_search_user_by_name_or_building(monkeypatch):
    mock_user_data = {
        "Alice": {"building": "A"},
        "Bob": {"building": "B"},
    }

    def mock_load_user_data():
        return mock_user_data

    monkeypatch.setattr(app.browse, "load_user_data", mock_load_user_data)

    result, error = search_user_by_name_or_building("Alice", "")
    assert result["name"] == "Alice"
    assert error is None

    result, error = search_user_by_name_or_building("", "B")
    assert result["name"] == "Bob"
    assert error is None

    result, error = search_user_by_name_or_building("Charlie", "")
    assert result is None
    assert error == "No user found with the given details."

    result, error = search_user_by_name_or_building("", "")
    assert result is None
    assert error == "Please enter a name or building!"
