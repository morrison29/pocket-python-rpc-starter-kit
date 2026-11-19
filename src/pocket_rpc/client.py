"""A minimal JSON-RPC client implemented with Python's standard library."""

import json
from typing import Any, List, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class PocketRPCError(RuntimeError):
    """Raised when an RPC request fails or returns an invalid response."""


class PocketRPCClient:
    """Call a Pocket-compatible JSON-RPC endpoint over HTTP POST."""

    def __init__(self, endpoint: str, timeout: float = 20.0) -> None:
        if not endpoint.startswith(("https://", "http://")):
            raise ValueError("endpoint must start with http:// or https://")
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")
        self.endpoint = endpoint
        self.timeout = timeout
        self._request_id = 1

    def call(self, method: str, params: Optional[List[Any]] = None) -> Any:
        """Call a JSON-RPC method and return its result."""
        if not method or not isinstance(method, str):
            raise ValueError("method must be a non-empty string")
        if params is None:
            params = []
        if not isinstance(params, list):
            raise ValueError("params must be a list")

        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": self._request_id,
        }
        self._request_id += 1
        body = json.dumps(payload).encode("utf-8")
        request = Request(
            self.endpoint,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=self.timeout) as response:
                raw_body = response.read().decode("utf-8")
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise PocketRPCError(f"HTTP {exc.code}: {detail or exc.reason}") from exc
        except (URLError, TimeoutError, OSError) as exc:
            raise PocketRPCError(f"Network request failed: {exc}") from exc

        try:
            data = json.loads(raw_body)
        except json.JSONDecodeError as exc:
            raise PocketRPCError("Endpoint returned invalid JSON") from exc

        if not isinstance(data, dict):
            raise PocketRPCError("Endpoint returned an unexpected JSON-RPC response")
        if data.get("error") is not None:
            raise PocketRPCError(f"JSON-RPC error: {data['error']}")
        if "result" not in data:
            raise PocketRPCError("JSON-RPC response is missing the result field")
        return data["result"]

    def get_block_number(self) -> int:
        """Return the latest block number as a decimal integer."""
        result = self.call("eth_blockNumber")
        if not isinstance(result, str) or not result.startswith("0x"):
            raise PocketRPCError("eth_blockNumber returned an invalid hexadecimal result")
        try:
            return int(result, 16)
        except ValueError as exc:
            raise PocketRPCError("eth_blockNumber returned invalid hexadecimal data") from exc
