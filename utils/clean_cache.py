import os
import shutil


def remove_directories(base_path=None, dir_names=None):
    """
    Remove specified directories (e.g., __pycache__, .idea) in the provided base path and its subdirectories.

    :param base_path: The base path to start scanning (default: two levels up from the current script's location).
    :param dir_names: List of directory names to remove (default: ["__pycache__", ".idea"]).
    """
    # Default base path (two levels up from the current script's location)
    if base_path is None:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    # Default directories to remove
    if dir_names is None:
        dir_names = ["__pycache__", ".idea"]

    # Validate the base path
    if not os.path.exists(base_path):
        return

    for root, dirs, _ in os.walk(base_path):  # Walk through the base directory
        for dir_name in dir_names:
            if dir_name in dirs:
                target_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(target_path, ignore_errors=False)  # Remove directory
                except Exception as e:
                    print(f"Error removing {target_path}: {e}")


if __name__ == "__main__":
    remove_directories()
