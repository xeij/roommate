import pytest
from unittest.mock import MagicMock
from Admin import Admin

@pytest.fixture
def db_manager_mock():
    """Mock database manager."""
    return MagicMock()

@pytest.fixture
def admin(db_manager_mock):
    """Admin instance with mocked db_manager."""
    return Admin(db_manager_mock)

def test_review_flagged_messages(admin, db_manager_mock):
    db_manager_mock.execute_query.return_value.fetchall.return_value = [(1, 101, "Test message")]
    admin.review_flagged_messages()
    db_manager_mock.execute_query.assert_called_with('SELECT * FROM flagged_messages')

def test_ban_user(admin, db_manager_mock):
    db_manager_mock.execute_query.return_value.rowcount = 1
    admin.ban_user(101)
    db_manager_mock.execute_query.assert_called_with('UPDATE users SET status = ? WHERE id = ?', ('banned', 101))

def test_unban_user(admin, db_manager_mock):
    db_manager_mock.execute_query.return_value.rowcount = 1
    admin.unban_user(101)
    db_manager_mock.execute_query.assert_called_with('UPDATE users SET status = ? WHERE id = ?', ('active', 101))

def test_remove_message(admin, db_manager_mock):
    db_manager_mock.execute_query.return_value.rowcount = 1
    admin.remove_message(1)
    db_manager_mock.execute_query.assert_called_with('DELETE FROM messages WHERE id = ?', (1,))

def test_update_app_permissions(admin, db_manager_mock):
    db_manager_mock.execute_query.return_value.rowcount = 1
    admin.update_app_permissions('key', 'value')
    db_manager_mock.execute_query.assert_called_with('UPDATE app_settings SET value = ? WHERE key = ?', ('value', 'key'))
