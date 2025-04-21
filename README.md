# StegoDetector

Detect whether an image contains hidden data (steganography) or not, using a
simple PyTorch classifier

## Setup

No GPU is required for this.

This project was created using the tool [uv](https://docs.astral.sh/uv/). For consistency, I ask
that you utilize `uv` as well.

### Installing uv

```bash
# MacOS & Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```powershell
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Virtual Environment

The below command will download and install the appropriate Python version, create a virtual environment,
and then install all the necessary packages.

```bash
uv sync --extra cpu
```

Should you have an NVIDIA GPU that you wish to use, the below command will install PyTorch with CUDA
libraries as well.

```bash
uv sync --extra gpu
```

## Running

There's 3 steps to running this program:

1. Download and prepare data
2. Train model
3. Evaluate model

### Download and Prepare Data

Assuming you already have activated the virtual environment using the source command.

```bash
./scripts/download_and_extract_data.sh
python scripts/sample_files.py
./scripts/stego_embed.sh
python sample_files.py
```

### Train Model

```bash
python stegodetector/train.py
```

### Evaluate Model

```bash
python stegodetector/evaluate.py
```

### Train-Evaluate Together

The main script assumes that you have the data already prepared and will then train and evaluate a
model.

```bash
python main.py
```

## Notes

This project started out as a sideproject that [I](https://github.com/Dylan-Gresham) did for fun.
It was then used as a workshop for Boise State University's CyberAI Club on Monday April 21st, 2025.
