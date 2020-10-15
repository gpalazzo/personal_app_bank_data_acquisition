from pathlib import Path
from dotenv import load_dotenv


project_dir = str(Path(__file__).resolve().parents[3])
project_dir += "/setup_config_credentials"


def load_credentials():
    """Load credentials as environment variable from .env file
    """
    env_path = Path(project_dir) / 'credentials.env'
    load_dotenv(dotenv_path=env_path)


def load_config():
    """Load configurations as environment variable from .env file
    """
    env_path = Path(project_dir) / 'config.env'
    load_dotenv(dotenv_path=env_path)
