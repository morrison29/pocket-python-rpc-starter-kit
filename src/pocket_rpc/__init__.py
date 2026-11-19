"""Small, dependency-free JSON-RPC client for Pocket public RPC endpoints."""

from .client import PocketRPCClient, PocketRPCError

__all__ = ["PocketRPCClient", "PocketRPCError"]
