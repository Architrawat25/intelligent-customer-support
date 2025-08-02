"""
Script to update AI models from Colab
Run this after training new models in Colab
"""

import os
import tarfile
import shutil
from pathlib import Path

def update_models_from_colab(tar_file_path: str):
    """Update models from Colab export"""
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "app" / "data"

    print(f"Updating models from: {tar_file_path}")

    # Create backup of existing models
    backup_dir = data_dir / "backup"
    if data_dir.exists():
        if backup_dir.exists():
            shutil.rmtree(backup_dir)
        shutil.copytree(data_dir, backup_dir)
        print("Created backup of existing models")

    # Extract new models
    with tarfile.open(tar_file_path, 'r:gz') as tar:
        tar.extractall(project_root / "app")

    print("Models updated successfully!")
    print("New model files:")
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            print(f"   - {os.path.relpath(os.path.join(root, file), data_dir)}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python update_ai_models.py <path_to_tar_file>")
        sys.exit(1)

    update_models_from_colab(sys.argv[1])
