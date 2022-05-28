import json
import sys


class MDO:

    def __init__(self: object, configFile: str) -> None:
        self.configFile: str = configFile
        self.dataConfig: dict = {}
        self.__init()
        self.load()

    def __cleanup(self: object) -> None:
        for section, sectionData in self.dataConfig.items():
            for key, defaultvalue in sectionData.items():
                propertyName: str = self.__getPropertyName(section, key)
                if hasattr(self, propertyName):
                    delattr(self, propertyName)
        self.dataConfig: dict = {}

    def __eprint(self: object, *args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    def __getDict(self: object) -> dict:
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
        propertyName: str = section.lower().replace(' ', '') + '_' + key.lower().replace(' ', '')
        return propertyName

    def __init(self: object) -> None:
        self.__cleanup()
        self.setup()

    def add(self: object, section: str, key: str, default: any) -> None:
        sectionWork: str = section.upper()
        if sectionWork not in self.dataConfig:
            self.dataConfig[sectionWork] = {}
        if key not in self.dataConfig[sectionWork]:
            self.dataConfig[sectionWork][key] = default
        propertyName: str = self.__getPropertyName(sectionWork, key)
        self.__dict__[propertyName] = default

    def load(self: object) -> bool:
        self.__init()
        success: bool = False
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
                success = True
            except ValueError:
                self.__eprint('Invalid config file [' + '{}'.format(self.configFile) + '], abort')
        return success

    def save(self: object) -> bool:
        success: bool = False
        with open(self.configFile, 'w') as configfile:
            configData: dict = self.__getDict()
            json.dump(configData, configfile, indent=4, sort_keys=True)
            success = True
        return success

    def setup(self: object) -> None:
        pass
