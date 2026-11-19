"""Fetch the latest Ethereum block number through Pocket Network."""

import os
import sys
from pathlib import Path

# Allows running this example directly from a source checkout without installation.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pocket_rpc import PocketRPCClient, PocketRPCError  # noqa: E402

DEFAULT_ENDPOINT = "https://eth.api.pocket.network"
endpoint = os.environ.get("POCKET_RPC_URL", DEFAULT_ENDPOINT)

try:
    client = PocketRPCClient(endpoint)
    block_number = client.get_block_number()
    print("Pocket RPC test: SUCCESS")
    print(f"Latest Ethereum block: {block_number}")
except (PocketRPCError, ValueError) as error:
    print("Pocket RPC test: FAILED")
    print(f"Reason: {error}")
    raise SystemExit(1)
