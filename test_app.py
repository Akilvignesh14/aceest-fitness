from unittest.mock import MagicMock
from app import ACEestApp

def test_data_integrity():
    # Create a fake "root" so we don't need a real monitor
    mock_root = MagicMock()
    app_instance = ACEestApp(mock_root)

    # Verify the fitness data is loaded correctly
    assert len(app_instance.programs) > 0
    assert "Beginner (BG)" in app_instance.programs