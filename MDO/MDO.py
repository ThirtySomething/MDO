import json
import os
import sys


class MDO:
    """ Class to deal with dynamic object, mainly uses as config file
    """

    def __init__(self: object, configFile: str) -> None:
        """ Default constructor

        Args:
            configFile (str): Name of config file used
        """
        # Set name of config file
        self.configFile: str = configFile
        # Clear catalog of allowed settings
        self.dataConfig: dict = {}
        # Load default values
        self.setup()
        # Update with config values
        self.load()

    def __cleanup(self: object) -> None:
        """ Remove configured dynamic attributes from class and
            cleanup internal catalog of allowed settings
        """
        for section, sectionData in self.dataConfig.items():
            for key, defaultvalue in sectionData.items():
                propertyName: str = self.__getPropertyName(section, key)
                if hasattr(self, propertyName):
                    delattr(self, propertyName)
        self.dataConfig: dict = {}

    def __eprint(self: object, *args, **kwargs):
        """ Print error messages
        """
        print(*args, file=sys.stderr, **kwargs)

    def __getDict(self: object) -> dict:
        """ Create dictionary from properties

        Returns:
            dict: Dictionary of properties
        """
        dictObject: dict = {}
        for section, sectionData in self.dataConfig.items():
            sectionWork: str = section.upper()
            if sectionWork not in dictObject:
                dictObject[sectionWork] = {}
            for key, defaultvalue in sectionData.items():
                if key not in dictObject[sectionWork]:
                    dictObject[sectionWork][key] = defaultvalue
                propertyName: str = self.__getPropertyName(sectionWork, key)
                dictObject[sectionWork][key] = self.__dict__[propertyName]
        return dictObject

    def __getPropertyName(self: object, section: str, key: str) -> str:
        """ Get unified name of property

        Args:
            section (str): Section name of property
            key (str): Property name

        Returns:
            str: Unified property name
        """
        propertyName: str = section.lower().replace(' ', '') + '_' + key.lower().replace(' ', '')
        return propertyName

    def __str__(self):
        """ Get dictionary as string
        """
        return json.dumps(self.dataConfig, indent=3)

    def __repr__ (self):
        """ Get dictionary as string
        """
        return self.__str__()

    def add(self: object, section: str, key: str, default: any) -> None:
        """ Used to define a property

        Args:
            section (str): Section name of property
            key (str): Name of property
            default (any): Default value of property
        """
        sectionWork: str = section.upper()
        if sectionWork not in self.dataConfig:
            self.dataConfig[sectionWork] = {}
        if key not in self.dataConfig[sectionWork]:
            self.dataConfig[sectionWork][key] = default
        propertyName: str = self.__getPropertyName(sectionWork, key)
        self.__dict__[propertyName] = default

    def load(self: object) -> bool:
        """ Load properties from config file

        Returns:
            bool: True on succes, otherwise False
        """
        self.__cleanup()
        self.setup()
        success: bool = False
        if not os.path.exists(self.configFile):
            return success
        with open(self.configFile, 'r') as configfile:
            try:
                configRead = json.load(configfile)
                for section, sectionData in configRead.items():
                    sectionWork: str = section.upper()
                    if sectionWork in self.dataConfig:
                        for key, datavalue in sectionData.items():
                            if key in self.dataConfig[section]:
                                propertyName: str = self.__getPropertyName(section, key)
                                self.__dict__[propertyName] = datavalue
                                self.dataConfig[sectionWork][key] = datavalue
                success = True
            except ValueError:
                self.__eprint('Invalid config file [' + '{}'.format(self.configFile) + '], abort')
        return success

    def save(self: object) -> bool:
        """ Save properties to file

        Returns:
            bool: True on succes, otherwise False
        """
        success: bool = False
        with open(self.configFile, 'w') as configfile:
            configData: dict = self.__getDict()
            json.dump(configData, configfile, indent=4, sort_keys=True)
            success = True
        return success

    def setup(self: object) -> None:
        """ Dummy method, needs to be overwritten by child class
        """
        pass
