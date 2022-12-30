from dotenv import dotenv_values
from pathlib import Path  # Python 3.6+ only

env_path = Path('.') / '.env.local'

config = dotenv_values(dotenv_path=env_path)
