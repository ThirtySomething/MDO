import json
import os
import sys
from typing import Any

# https://gist.github.com/fumingshih/49c1e04e1bee7caa06a9


class MDO:
    """Class to deal with dynamic object, mainly uses as config file"""

    def __init__(self, config_file_name: str, auto_load: bool = True) -> None:
        """Default constructor

        Args:
            config_file_name (str): Name of config file used
            auto_load (bool): Load persisted config during initialization
        """
        # Set name of config file
        self._config_file_name: str = config_file_name
        # Define properties in cleanup method
        self._cleanup()
        # Load default values
        self.setup()
        # Update with config values when requested
        if auto_load:
            self.load()

    def __str__(self) -> str:
        """Get dictionary as string"""
        return json.dumps(self._data, indent=4)

    def __repr__(self) -> str:
        """Get dictionary as string"""
        return self.__str__()

    def add(self, section: str, key: str, default: Any) -> None:
        """Used to define a property

        Args:
            section (str): Section name of property
            key (str): Name of property
            default (Any): Default value of property
        """
        # Write to defaults
        self._set_dictionary_entry(self._defaults, section, key, default)
        # Also write to used data
        self._set_dictionary_entry(self._data, section, key, default)

    def _cleanup(self) -> None:
        """Cleanup internal data"""
        # Dictionary to define allowed sections, keys and defaults
        self._defaults: dict = {}
        # Dictionary to memorized real used data
        self._data: dict = {}

    def _eprint(self, *args, **kwargs) -> None:
        """Print error messages"""
        print(*args, file=sys.stderr, **kwargs)

    def _validate_config_data(self, config_data: Any) -> bool:
        """Validate the expected config structure.

        The file content must be a dictionary whose values are dictionaries.

        Args:
            config_data (Any): Data loaded from JSON.

        Returns:
            bool: True if the shape is valid, otherwise False.
        """
        if not isinstance(config_data, dict):
            return False
        for section_data in config_data.values():
            if not isinstance(section_data, dict):
                return False
        return True

    def load(self) -> bool:
        """Load data from config file

        Returns:
            bool: True on succes, otherwise False
        """
        # Erase internal storage
        self._cleanup()
        # Set defaults
        self.setup()
        # Assume failure by default
        success: bool = False
        if not os.path.exists(self._config_file_name):
            # Config file does not exist, abort
            return success
        try:
            with open(self._config_file_name, "r", encoding="utf-8") as config_file:
                # Read data from file
                config_read = json.load(config_file)
                if not self._validate_config_data(config_read):
                    raise ValueError()
                for section, section_data in config_read.items():
                    for key, data_value in section_data.items():
                        self._set_dictionary_entry(self._data, section, key, data_value)
                # Set success
                success = True
        except (OSError, ValueError, TypeError) as ex:
            self._eprint(f"Invalid config file [{self._config_file_name}]: [{ex}]")
        return success

    def save(self) -> bool:
        """Save properties to file

        Returns:
            bool: True on succes, otherwise False
        """
        success: bool = False
        data_stripped: dict = {}
        for section, section_data in self._defaults.items():
            for key, dummy in section_data.items():
                if section not in data_stripped:
                    data_stripped[section] = {}
                data_stripped[section][key] = self.value_get(section, key)
        try:
            with open(self._config_file_name, "w", encoding="utf-8") as config_file:
                json.dump(data_stripped, config_file, indent=4, sort_keys=True)
                success = True
        except (OSError, TypeError, ValueError) as ex:
            self._eprint(f"Unable to save config file [{self._config_file_name}]: [{ex}]")
        return success

    def _set_dictionary_entry(self, dictionary: dict, section: str, key: str, value: Any) -> None:
        """Set value to dictionary

        Args:
            self (object): Instance
            dictionary (dict): Dictionary to store data
            section (str): Section used
            key (str): Key used
            value (Any): Value to set
        """
        section_work: str = section.upper().strip()
        if section_work not in dictionary:
            dictionary[section_work] = {}
        key_work: str = key.strip()
        dictionary[section_work][key_work] = value

    def setup(self) -> None:
        """Dummy method, needs to be overwritten by child class"""
        pass

    def value_get(self, section: str, key: str) -> Any:
        """Get value from object

        Args:
            self (object): Instance
            section (str): Section used
            key (str): Key used

        Returns:
            Any: None or the value saved
        """
        section_work: str = section.upper().strip()
        key_work: str = key.strip()
        if section_work not in self._data:
            return None
        if key_work not in self._data[section_work]:
            return None
        return self._data[section_work][key_work]

    def value_set(self, section: str, key: str, value: Any) -> None:
        """Set value to object

        Args:
            self (object): Instance
            section (str): Section used
            key (str): Key used
            value (Any): Value to set
        """
        self._set_dictionary_entry(self._data, section, key, value)
