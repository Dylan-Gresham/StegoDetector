# StegoDetector

Detect whether an image contains hidden data (steganography) or not, using a
simple PyTorch classifier

## Setup

No GPU is required for this. If you prefer to use standard Python virtual
environments, execute the following three commands to setup your environment.

```bash
python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

If you like to utilize [uv](https://docs.astral.sh/uv/) execute the following
command.

```bash
uv sync --extra cpu
```
