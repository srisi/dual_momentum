from pathlib import Path
import socket

if socket.gethostname() == 'Stephans-MacBook-Pro.local':
    DATA_PATH = Path('/dual_momentum_data')
else:
    DATA_PATH = Path(Path(__file__).parent.parent, 'data')
