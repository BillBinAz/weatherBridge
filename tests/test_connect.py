import unittest
from unittest.mock import patch, MagicMock
from utilities import connect


class TestConnect(unittest.TestCase):

    @patch('utilities.connect.new_client_from_environment')
    def test_get_credentials_success(self, mock_client_func):
        """Test successful credential retrieval."""
        mock_client = MagicMock()
        mock_item = MagicMock()
        mock_item.fields = ["field1", "field2"]
        mock_client.get_item.return_value = mock_item
        mock_client_func.return_value = mock_client

        result = connect.get_credentials("test_item_id")
        self.assertEqual(result, ["field1", "field2"])
        mock_client.get_item.assert_called_once_with("test_item_id", connect.AUTOMATION_VAULT_ID)

    @patch('utilities.connect.new_client_from_environment')
    def test_get_credentials_failure(self, mock_client_func):
        """Test credential retrieval failure."""
        mock_client_func.side_effect = Exception("Connection error")

        result = connect.get_credentials("test_item_id")
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
