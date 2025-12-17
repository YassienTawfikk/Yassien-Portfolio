import os
import shutil


def remove_directories(base_path=None, dir_names=None):
    """
    Remove specified directories (e.g., __pycache__, .idea) in the provided base path.
    """
    # Default base path
    if base_path is None:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    if dir_names is None:
        dir_names = ["__pycache__", ".idea"]

    if not os.path.exists(base_path):
        return

    for root, dirs, _ in os.walk(base_path):
        for dir_name in dir_names:
            if dir_name in dirs:
                target_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(target_path, ignore_errors=False)
                except Exception as e:
                    print(f"Error removing {target_path}: {e}")
