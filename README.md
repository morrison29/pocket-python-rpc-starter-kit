# Pocket Python RPC Starter Kit

A small, beginner-friendly Python project for calling an Ethereum JSON-RPC method through Pocket Network. The included example retrieves the latest Ethereum block number.

- **Language:** Python 3.8+
- **Dependencies:** Python standard library only
- **Default endpoint:** `https://eth.api.pocket.network`
- **Credentials:** No API key, wallet, or private key is needed for this public-endpoint example.

## What this project demonstrates

1. Sending an HTTP POST JSON-RPC request.
2. Calling `eth_blockNumber`.
3. Handling network, HTTP, and JSON-RPC errors.
4. Converting the hexadecimal block result into a decimal integer.

## Prerequisites

- Python 3.8 or newer
- Git (only if cloning the repository)
- Internet access for the live example

## Quick start

Clone the repository and enter its directory:

```bash
git clone https://github.com/YOUR-USERNAME/pocket-python-rpc-starter-kit.git
cd pocket-python-rpc-starter-kit
```

Run the example directly (no third-party packages required):

```bash
python examples/get_block.py
```

On systems where Python is invoked as `python3`:

```bash
python3 examples/get_block.py
```

Expected output (the block number changes over time):

```text
Pocket RPC test: SUCCESS
Latest Ethereum block: <current block number>
```

## Use a different compatible endpoint

The example reads an optional `POCKET_RPC_URL` environment variable. If it is not set, it uses the public Ethereum endpoint above.

PowerShell:

```powershell
$env:POCKET_RPC_URL = "https://eth.api.pocket.network"
python examples/get_block.py
```

macOS/Linux:

```bash
export POCKET_RPC_URL="https://eth.api.pocket.network"
python3 examples/get_block.py
```

Do not put private credentials in source code or commit them to Git.

## Use the client in your own code

The reusable client is in `src/pocket_rpc/client.py`:

```python
from pocket_rpc import PocketRPCClient

client = PocketRPCClient("https://eth.api.pocket.network")
block_number = client.get_block_number()
print(block_number)
```

To call another Ethereum JSON-RPC method:

```python
result = client.call("eth_chainId")
print(result)
```

## Run the automated tests

The tests use mocked HTTP responses. They do not require an internet connection and do not make paid requests.

```bash
python -m unittest discover -s tests -v
```

## Clean-environment validation

Create and activate a virtual environment:

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m unittest discover -s tests -v
python examples/get_block.py
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m unittest discover -s tests -v
python examples/get_block.py
```

No `pip install` step is needed because the client and tests use only Python's standard library.

## Troubleshooting

- **`python` is not recognised:** Install Python 3.8+ and ensure it is on your PATH; try `py` on Windows or `python3` on macOS/Linux.
- **Network or timeout error:** Check your connection and retry. The public endpoint may be temporarily unavailable.
- **HTTP error:** The endpoint may be rate-limited or unavailable. Review the response message and retry later.
- **Unexpected JSON-RPC result:** Confirm that the endpoint supports the requested method and returns a standard JSON-RPC response.

## Limitations and safe use

- This is a learning starter, not a production-ready high-availability RPC system.
- Public endpoint availability, rate limits, and performance may change.
- Validate blockchain data before relying on it for important decisions.
- Never commit private keys, payment credentials, tokens, or other secrets.

## References

- Pocket API Portal: https://docs.pocket.network/foundation/api-portal/
- Pocket public RPC endpoints: https://api.pocket.network/
- Ethereum JSON-RPC documentation: https://ethereum.org/developers/docs/apis/json-rpc/

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Please include reproducible steps and tests for changes.

## License

MIT. See [LICENSE](LICENSE).
