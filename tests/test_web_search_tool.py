import unittest
import json
from unittest.mock import patch, Mock
from crew_automation_content_editor_launcher.tools.web_search_tool import WebSearchTool
from crew_automation_content_editor_launcher.utils.config_manager import ConfigManager

class TestWebSearchTool(unittest.TestCase):
    @patch.object(ConfigManager, 'get_api_key')
    @patch('requests.request')
    def test_search_request_structure(self, mock_request, mock_get_api_key):
        # Configure test API key
        mock_get_api_key.return_value = 'test_serper_key'
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'organic': []}
        mock_request.return_value = mock_response

        # Instantiate and run the tool
        tool = WebSearchTool()
        result = tool._run("test query", 3)

        # Verify API key propagation
        mock_get_api_key.assert_called_with("serper")
        
        # Verify request headers
        headers = mock_request.call_args[1]['headers']
        self.assertEqual(headers['X-API-KEY'], 'test_serper_key')
        self.assertEqual(headers['Content-Type'], 'application/json')
        self.assertEqual(headers['User-Agent'], 'CrewAI/1.0 (Siebert_Content_Crew)')

        # Verify payload structure
        payload = json.loads(mock_request.call_args[1]['data'])
        self.assertEqual(payload['q'], "test query")
        self.assertEqual(payload['num'], 3)
        self.assertEqual(payload['page'], 1)
        self.assertEqual(payload['hl'], "en")

        # Verify result handling
        self.assertIn("Search results for 'test query'", result)

if __name__ == '__main__':
    unittest.main()