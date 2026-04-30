import os
import tempfile
import unittest

from MDO.MDO import MDO


class dataTest(MDO):
    def setup(self) -> None:
        self.add("s1", "k1", "v1")
        self.add("s1", "k2", 42)
        self.add("s2", "k3", "v2")


class MDOtest(unittest.TestCase):
    testConfigfile: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config_test.json")

    @classmethod
    def deleteFile(cls) -> None:
        # Ensure config file does not exist
        if os.path.exists(MDOtest.testConfigfile):
            os.remove(MDOtest.testConfigfile)

    @classmethod
    def setUpClass(cls) -> None:
        MDOtest.deleteFile()

    def test_01_init(self) -> None:
        """Test initialization"""
        sut: dataTest = dataTest(MDOtest.testConfigfile)
        self.assertEqual(hasattr(sut, "_config_file_name"), True, "Property for config filename does not exist")
        self.assertEqual(hasattr(sut, "_defaults"), True, "Dictionary for defaults does not exist")
        self.assertEqual(hasattr(sut, "_data"), True, "Dictionary for data does not exist")

    def test_02_defaultvalues(self) -> None:
        """Test of default values"""
        # Section, key, value to compare
        data_list = [("s1", "k1", "v1"), ("s1", "k2", 42), ("s2", "k3", "v2"), ("s3", "k3", None)]
        # Init with default values
        sut: dataTest = dataTest(MDOtest.testConfigfile)
        # Test section, key, values
        for record in data_list:
            self.assertEqual(record[2] == sut.value_get(record[0], record[1]), True, "Default value invalid")

    def test_03_modify(self) -> None:
        """Test of modifying values"""
        # Section, key, value, value new
        data_list = [("s1", "k1", "v1", "v2"), ("s1", "k2", 42, "v3"), ("s2", "k3", "v2", 42), ("s3", "k3", None, None)]
        # Init with default values
        sut: dataTest = dataTest(MDOtest.testConfigfile)
        # Test section, key, values and new values
        for record in data_list:
            self.assertEqual(record[2] == sut.value_get(record[0], record[1]), True, "Default value invalid")
            sut.value_set(record[0], record[1], record[3])
            self.assertEqual(record[3] == sut.value_get(record[0], record[1]), True, "Modified value invalid")

    def test_04_save_explicit(self) -> None:
        """Test save of config"""
        # Section, key, value, value new
        data_list = [("s1", "k1", "v1", "v2"), ("s1", "k2", 42, "v3"), ("s2", "k3", "v2", 42), ("s3", "k3", None, None)]
        # Init with default values
        sut: dataTest = dataTest(MDOtest.testConfigfile)
        # Test section, key, values and new values
        for record in data_list:
            self.assertEqual(record[2] == sut.value_get(record[0], record[1]), True, "Default value invalid")
            sut.value_set(record[0], record[1], record[3])
            self.assertEqual(record[3] == sut.value_get(record[0], record[1]), True, "Modified value invalid")
        # Up to now not persistent
        self.assertEqual(os.path.exists(MDOtest.testConfigfile), False, ("Config file [{}] already exists.".format(MDOtest.testConfigfile)))
        # Save
        self.assertEqual(sut.save(), True, ("Config file [{}] not saved.".format(MDOtest.testConfigfile)))
        # Configfile must exists
        self.assertEqual(os.path.exists(MDOtest.testConfigfile), True, ("Config file [{}] missing.".format(MDOtest.testConfigfile)))

    def test_05_load_implizit(self) -> None:
        """Implizit load of config"""
        # Section, key, value, value new
        data_list = [("s1", "k1", "v2"), ("s1", "k2", "v3"), ("s2", "k3", 42), ("s3", "k3", None)]
        # Configfile must exists
        self.assertEqual(os.path.exists(MDOtest.testConfigfile), True, ("Config file [{}] missing.".format(MDOtest.testConfigfile)))
        # Init with default values
        sut: dataTest = dataTest(MDOtest.testConfigfile)
        # Test section, key, and values
        for record in data_list:
            value = sut.value_get(record[0], record[1])
            self.assertEqual(record[2] == value, True, "Read invalid data, expected [{}], but got [{}]".format(record[2], value))

    def test_06_load_invalid_json(self) -> None:
        """Invalid JSON keeps defaults and reports failure"""
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as config_file:
            config_file.write('{"s1": {"k1": "broken"')
            config_path = config_file.name
        try:
            sut: dataTest = dataTest(config_path)
            self.assertEqual(sut.load(), False, "Invalid JSON should fail to load")
            self.assertEqual(sut.value_get("s1", "k1"), "v1", "Defaults should remain after invalid JSON")
            self.assertEqual(sut.value_get("s1", "k2"), 42, "Defaults should remain after invalid JSON")
        finally:
            if os.path.exists(config_path):
                os.remove(config_path)

    def test_07_normalize_section_and_key_names(self) -> None:
        """Section and key names are normalized on load, set and get"""
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as config_file:
            config_file.write('{" s1 ": {" k1 ": "loaded value"}}')
            config_path = config_file.name
        try:
            sut: dataTest = dataTest(config_path)
            self.assertEqual(sut.value_get(" S1 ", " k1 "), "loaded value", "Loaded values should normalize whitespace and case")
            sut.value_set(" s1 ", " k1 ", "updated value")
            self.assertEqual(sut.value_get("S1", "k1"), "updated value", "Runtime writes should normalize whitespace and case")
        finally:
            if os.path.exists(config_path):
                os.remove(config_path)

    def test_08_save_raises_on_invalid_path(self) -> None:
        """Saving to an invalid path surfaces the underlying filesystem error"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = os.path.join(temp_dir, "missing", "config.json")
            sut: dataTest = dataTest(config_path)
            with self.assertRaises(OSError):
                sut.save()

    @classmethod
    def tearDownClass(cls) -> None:
        MDOtest.deleteFile()
