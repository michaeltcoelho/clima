from pathlib import Path

import pytest

PATH = Path(__file__).parent


@pytest.fixture
def mock_loader():
    def load_file(mock_filename):
        mock_path = PATH / f'mocks/{mock_filename}'
        with open(str(mock_path), encoding='utf8') as mock_file:
            return mock_file.read()
    return load_file
