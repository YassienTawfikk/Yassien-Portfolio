import json


def load_json(file_path):
    """
    Load JSON data from the specified file.
    :param file_path: Path to the JSON file.
    :return: Parsed JSON data as a dictionary or list, or None if an error occurs.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} contains invalid JSON.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def get_json_values(file_path, queries):
    """
    Fetch multiple values from a JSON file by traversing potentially nested dictionaries or lists.
    :param file_path: Path to the JSON file.
    :param queries: List of tuples containing the keys (or indices) to traverse in order.
    :return: List of values corresponding to each query.
    """
    data = load_json(file_path)
    if data is None:
        print("Error: No data loaded from JSON.")
        return [None for _ in queries]

    results = []
    for query in queries:
        value = data
        for key in query:
            if isinstance(key, int):
                if isinstance(value, list) and 0 <= key < len(value):
                    value = value[key]
                else:
                    print(f"Index '{key}' not found (out of range or not a list) at current step.")
                    value = None
                    break
                    value = None
                    break
            else:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    print(f"Key '{key}' not found at current step.")
                    value = None
                    break
        results.append(value)

    return results if len(results) > 1 else results[0]  # Return a single value if only one query
