import sys
from pathlib import Path

from backend.app import create_app

# Add the root directory to the Python path
root_dir = str(Path(__file__).parent)
sys.path.append(root_dir)

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
