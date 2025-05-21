import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

# Ensure app.main can be imported.
# If your project structure is different, you might need to adjust the Python path.
# For this environment, we assume the tests are run from the root directory or that PYTHONPATH is set up.
from app.main import app

client = TestClient(app)

# Dummy payload for POST requests
dummy_issue_payload = {"title": "Test title", "body": "Test body"}

class TestApiAuth(unittest.TestCase):

    def test_missing_api_key(self):
        """
        Test Case 1: Missing API Key
        FastAPI's APIKeyHeader by default returns 403 if the header is missing.
        """
        with patch.dict(os.environ, {"VALID_API_KEYS": "testkey"}, clear=True):
            response = client.post("/v1/fossistant/difficulty/", json=dummy_issue_payload)
        # Default behavior for a missing APIKeyHeader is 403
        # Our custom logic for an *empty* key (which would be 401) isn't hit if the header is absent.
        self.assertEqual(response.status_code, 403)
        # The detail for a missing header by APIKeyHeader is typically "Not authenticated"
        # or similar, let's check if "Not authenticated" is present.
        # This can vary slightly based on FastAPI versions or configurations.
        self.assertIn("Not authenticated", response.json().get("detail", "").lower())


    @patch.dict(os.environ, {}, clear=True) # Start with a clean environment for this test
    def test_invalid_api_key(self):
        """
        Test Case 2: Invalid API Key
        """
        os.environ["VALID_API_KEYS"] = "testkey"
        response = client.post(
            "/v1/fossistant/difficulty/",
            headers={"X-API-Key": "invalidkey"},
            json=dummy_issue_payload
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Invalid API Key"})
        del os.environ["VALID_API_KEYS"] # Clean up

    @patch.dict(os.environ, {}, clear=True)
    def test_valid_api_key(self):
        """
        Test Case 3: Valid API Key
        """
        os.environ["VALID_API_KEYS"] = "testkey"
        response = client.post(
            "/v1/fossistant/difficulty/",
            headers={"X-API-Key": "testkey"},
            json=dummy_issue_payload
        )
        self.assertEqual(response.status_code, 200)
        # Check for expected keys in the successful response
        self.assertIn("difficulty", response.json())
        self.assertIn("score", response.json())
        del os.environ["VALID_API_KEYS"] # Clean up

    @patch.dict(os.environ, {}, clear=True) # Start with a clean environment
    def test_server_misconfiguration_no_keys_set(self):
        """
        Test Case 4: Server Misconfiguration (VALID_API_KEYS not set)
        """
        # Ensure VALID_API_KEYS is not in environ or is empty
        if "VALID_API_KEYS" in os.environ:
            del os.environ["VALID_API_KEYS"]

        response = client.post(
            "/v1/fossistant/difficulty/",
            headers={"X-API-Key": "anykey"},
            json=dummy_issue_payload
        )
        self.assertEqual(response.status_code, 500)
        # Based on the auth.py implementation
        self.assertEqual(response.json(), {"detail": "Server misconfiguration: VALID_API_KEYS not set"})

    @patch.dict(os.environ, {}, clear=True)
    def test_server_misconfiguration_empty_keys_set(self):
        """
        Test Case 4 (variant): Server Misconfiguration (VALID_API_KEYS is empty string)
        """
        os.environ["VALID_API_KEYS"] = "" # Set to empty string
        response = client.post(
            "/v1/fossistant/difficulty/",
            headers={"X-API-Key": "anykey"},
            json=dummy_issue_payload
        )
        self.assertEqual(response.status_code, 500)
        # Based on the auth.py implementation
        self.assertEqual(response.json(), {"detail": "Server misconfiguration: VALID_API_KEYS not set"})
        del os.environ["VALID_API_KEYS"] # Clean up

if __name__ == "__main__":
    unittest.main()
