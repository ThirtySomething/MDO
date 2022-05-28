import unittest
from MDO.MDO import MDO


class dataTest(MDO):
    def setup(self: object) -> bool:
        self.add('section', 'key1', 'default')
        self.save()


class MDOtest(unittest.TestCase):
    testConfigfile: str = 'config_test.json'

    def test_init(self: object):
        sut: dataTest = dataTest(self.testConfigfile)
        self.assertEqual(hasattr(sut, 'configFile'), True, 'Property for config filename does not exist')
        self.assertEqual(hasattr(sut, 'dataConfig'), True, 'Has attribute about section, keys and defaults')

    def test_configvalue(self: object):
        sut: dataTest = dataTest(self.testConfigfile)
        self.assertEqual(hasattr(sut, 'section_key1'), True, 'Property section_key1 does not exist')
