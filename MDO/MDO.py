import json
import os
import sys
from collections import OrderedDict

# https://gist.github.com/fumingshih/49c1e04e1bee7caa06a9


class MDO:
    """Class to deal with dynamic object, mainly uses as config file"""

    def __init__(self: object, config_file_name: str) -> None:
        """Default constructor

        Args:
            config_file_name (str): Name of config file used
        """
        # Set name of config file
        self._config_file_name: str = config_file_name
        # Define properties in cleanup method
        self.cleanup()
        # Load default values
        self.setup()
        # Update with config values
        self.load()

    def __str__(self: object) -> str:
        """Get dictionary as string"""
        return json.dumps(self._data, indent=4)

    def __repr__(self: object) -> str:
        """Get dictionary as string"""
        return self.__str__()

    def add(self: object, section: str, key: str, default: any) -> None:
        """Used to define a property

        Args:
            section (str): Section name of property
            key (str): Name of property
            default (any): Default value of property
        """
        # Write to defaults
        self.set_dictionary_entry(self._defaults, section, key, default)
        # Also write to used data
        self.set_dictionary_entry(self._data, section, key, default)

    def cleanup(self: object) -> None:
        """Cleanup internal data"""
        # Dictionary to define allowed sections, keys and defaults
        self._defaults: dict = {}
        # Dictionary to memorized real used data
        self._data: dict = {}

    def eprint(self: object, *args, **kwargs) -> None:
        """Print error messages"""
        print(*args, file=sys.stderr, **kwargs)

    def load(self: object) -> bool:
        """Load data from config file

        Returns:
            bool: True on succes, otherwise False
        """
        # Erase internal storage
        self.cleanup()
        # Set defaults
        self.setup()
        # Assume failure by default
        success: bool = False
        if not os.path.exists(self._config_file_name):
            # Config file does not exist, abort
            return success
        with open(self._config_file_name, "r", encoding="utf-8") as config_file:
            # Read data from file
            try:
                config_read = json.load(config_file)
                for section, section_data in config_read.items():
                    for key, data_value in section_data.items():
                        self.set_dictionary_entry(self._data, section, key, data_value)
                # Set success
                success = True
            except ValueError:
                self.eprint("Invalid config file [%s], abort", self._config_file_name)
        return success

    def save(self: object) -> bool:
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
        data_stripped = OrderedDict(sorted(data_stripped.items()))
        with open(self._config_file_name, "w", encoding="utf-8") as config_file:
            json.dump(data_stripped, config_file, indent=4, sort_keys=True)
            success = True
        return success

    def set_dictionary_entry(self: object, dictionary: dict, section: str, key: str, value: any) -> None:
        """Set value to dictionary

        Args:
            self (object): Instance
            dictionary (dict): Dictionary to store data
            section (str): Section used
            key (str): Key used
            value (any): Value to set
        """
        section_work: str = section.upper().strip()
        if section_work not in dictionary:
            dictionary[section_work] = {}
        key_work: str = key.strip()
        dictionary[section_work][key_work] = value

    def setup(self: object) -> None:
        """Dummy method, needs to be overwritten by child class"""
        pass

    def value_get(self: object, section: str, key: str) -> any:
        """Get value from object

        Args:
            self (object): Instance
            section (str): Section used
            key (str): Key used

        Returns:
            any: None or the value saved
        """
        section_work: str = section.upper()
        if section_work not in self._data:
            return None
        if key not in self._data[section_work]:
            return None
        return self._data[section_work][key]

    def value_set(self: object, section: str, key: str, value: any) -> None:
        """Set value to object

        Args:
            self (object): Instance
            section (str): Section used
            key (str): Key used
            value (any): Value to set
        """
        self.set_dictionary_entry(self._data, section, key, value)
