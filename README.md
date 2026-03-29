# IPL-2026
Predict who is going to win the 2026 IPL

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the package (with `src` on the path):

```bash
PYTHONPATH=src python -m ipl_pred
```

Run tests:

```bash
PYTHONPATH=src python -m unittest discover -s tests -p 'test_*.py'
```
