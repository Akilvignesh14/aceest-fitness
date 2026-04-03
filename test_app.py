from app import ACEestApp
import tkinter as tk

def test_data_integrity():
    # Setup a temporary "headless" window for the test
    root = tk.Tk()
    app_instance = ACEestApp(root)
    
    # Verify the fitness data dictionary is not empty
    assert len(app_instance.programs) > 0
    assert "Beginner (BG)" in app_instance.programs
    
    root.destroy()