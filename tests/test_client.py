import json
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pocket_rpc import PocketRPCClient, PocketRPCError


class FakeResponse:
    def __init__(self, body):
        self.body = body.encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.body


class PocketRPCClientTests(unittest.TestCase):
    def setUp(self):
        self.client = PocketRPCClient("https://eth.api.pocket.network")

    @patch("pocket_rpc.client.urlopen")
    def test_get_block_number_converts_hex_to_decimal(self, mocked_urlopen):
        mocked_urlopen.return_value = FakeResponse(
            json.dumps({"jsonrpc": "2.0", "id": 1, "result": "0x10"})
        )
        self.assertEqual(self.client.get_block_number(), 16)
        request = mocked_urlopen.call_args.args[0]
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(json.loads(request.data)["method"], "eth_blockNumber")

    @patch("pocket_rpc.client.urlopen")
    def test_rpc_error_is_reported(self, mocked_urlopen):
        mocked_urlopen.return_value = FakeResponse(
            json.dumps({"jsonrpc": "2.0", "id": 1, "error": {"code": -1, "message": "failed"}})
        )
        with self.assertRaisesRegex(PocketRPCError, "JSON-RPC error"):
            self.client.get_block_number()

    @patch("pocket_rpc.client.urlopen")
    def test_missing_result_is_reported(self, mocked_urlopen):
        mocked_urlopen.return_value = FakeResponse(json.dumps({"jsonrpc": "2.0", "id": 1}))
        with self.assertRaisesRegex(PocketRPCError, "missing the result"):
            self.client.call("eth_blockNumber")

    @patch("pocket_rpc.client.urlopen")
    def test_invalid_json_is_reported(self, mocked_urlopen):
        mocked_urlopen.return_value = FakeResponse("not-json")
        with self.assertRaisesRegex(PocketRPCError, "invalid JSON"):
            self.client.call("eth_blockNumber")

    def test_rejects_invalid_endpoint(self):
        with self.assertRaises(ValueError):
            PocketRPCClient("ftp://example.com")


if __name__ == "__main__":
    unittest.main()
