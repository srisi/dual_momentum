from pathlib import Path

# DATA_PATH = Path ('..', 'data')

print(Path(__file__).parent.parent)

DATA_PATH = Path(Path(__file__).parent.parent, 'data')
