import json


class ConfigFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_json()

    def load_json(self):
        try:
            with open(self.file_path, 'r') as file:
                self.data = json.load(file)
        except json.JSONDecodeError:
            raise (
                f"Error: Unable to parse JSON from file '{
                    self.file_path}'.")
        except FileNotFoundError:
            raise (f"Error: File '{self.file_path}' not found.")
        except PermissionError:
            raise (
                f"Error: Permission denied to read from file '{
                    self.file_path}'.")
        except IsADirectoryError:
            raise (f"Error: '{self.file_path}' is a directory.")
        except OSError:
            raise (f"Error: Unable to read from file '{self.file_path}'.")
        except Exception as e:
            raise (
                f"Error: An unexpected error occurred while reading from file '{
                    self.file_path}': {e}")

    def save_json(self):
        try:
            with open(self.file_path, 'w') as file:
                json.dump(self.data, file, indent=4)
        except TypeError:
            raise (
                f"Error: Unable to serialize data to JSON for file '{
                    self.file_path}'.")
        except FileNotFoundError:
            raise (f"Error: File '{self.file_path}' not found.")
        except PermissionError:
            raise (
                f"Error: Permission denied to write to file '{
                    self.file_path}'.")
        except IsADirectoryError:
            raise (f"Error: '{self.file_path}' is a directory.")
        except OSError:
            raise (f"Error: Unable to write to file '{self.file_path}'.")
        except Exception as e:
            raise (
                f"Error: An unexpected error occurred while writing to file '{
                    self.file_path}': {e}")

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save_json()
