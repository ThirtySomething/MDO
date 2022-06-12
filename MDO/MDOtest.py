import unittest
from MDO.MDO import MDO
import os


class dataTest(MDO):
    def setup(self: object) -> bool:
        self.add('s1', 'k1', 'v1')
        self.add('s1', 'k2', 42)
        self.add('s2', 'k3', 'v2')


class MDOtest(unittest.TestCase):
    testConfigfile: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config_test.json')

    @classmethod
    def setUpClass(cls):
        # Ensure config file does not exist
        if os.path.exists(MDOtest.testConfigfile):
            os.remove(MDOtest.testConfigfile)

    def test_01_init(self: object):
        """ Test initialization
        """
        sut: dataTest = dataTest(MDOtest.testConfigfile)
        self.assertEqual(hasattr(sut, 'configFile'), True, 'Property for config filename does not exist')
        self.assertEqual(hasattr(sut, 'dataConfig'), True, 'Has attribute about section, keys and defaults')

    def test_02_defaultvalues(self: object):
        """ Test of default values
        """
        # Init with default values
        sut: dataTest = dataTest(MDOtest.testConfigfile)
        # Property 1
        self.assertEqual(hasattr(sut, 's1_k1'), True, 'Property s1_k1 does not exist')
        self.assertEqual('v1' == sut.s1_k1, True, 'Default of s1_k1 is invalid')
        # Property 2
        self.assertEqual(hasattr(sut, 's1_k2'), True, 'Property s1_k2 does not exist')
        self.assertEqual(42 == sut.s1_k2, True, 'Default of s1_k2 is invalid')
        # Property 3
        self.assertEqual(hasattr(sut, 's2_k3'), True, 'Property s2_k3 does not exist')
        self.assertEqual('v2' == sut.s2_k3, True, 'Default of s2_k3 is invalid')

    def test_03_modify(self: object):
        """ Test of modifying values
        """
        # Init with default values
        sut: dataTest = dataTest(MDOtest.testConfigfile)
        # Property 1
        self.assertEqual(hasattr(sut, 's1_k1'), True, 'Property s1_k1 does not exist')
        self.assertEqual('v1' == sut.s1_k1, True, 'Default of s1_k1 is invalid')
        # Property 2
        self.assertEqual(hasattr(sut, 's1_k2'), True, 'Property s1_k2 does not exist')
        self.assertEqual(42 == sut.s1_k2, True, 'Default of s1_k2 is invalid')
        # Property 3
        self.assertEqual(hasattr(sut, 's2_k3'), True, 'Property s2_k3 does not exist')
        self.assertEqual('v2' == sut.s2_k3, True, 'Default of s2_k3 is invalid')
        # Modify propoerty 3
        sut.s2_k3 = 42
        # Property 3
        self.assertEqual(hasattr(sut, 's2_k3'), True, 'Property s2_k3 does not exist')
        self.assertEqual(42 == sut.s2_k3, True, 'Default of s2_k3 is invalid')

    def test_04_save_explicit(self: object):
        """ Test save of config
        """
        # Init with default values
        sut: dataTest = dataTest(MDOtest.testConfigfile)
        # Property 1
        self.assertEqual(hasattr(sut, 's1_k1'), True, 'Property s1_k1 does not exist')
        self.assertEqual('v1' == sut.s1_k1, True, 'Default of s1_k1 is invalid')
        # Property 2
        self.assertEqual(hasattr(sut, 's1_k2'), True, 'Property s1_k2 does not exist')
        self.assertEqual(42 == sut.s1_k2, True, 'Default of s1_k2 is invalid')
        # Property 3
        self.assertEqual(hasattr(sut, 's2_k3'), True, 'Property s2_k3 does not exist')
        self.assertEqual('v2' == sut.s2_k3, True, 'Default of s2_k3 is invalid')
        # Modify propoerty 3
        sut.s2_k3 = 42
        # Property 3
        self.assertEqual(hasattr(sut, 's2_k3'), True, 'Property s2_k3 does not exist')
        self.assertEqual(42 == sut.s2_k3, True, 'Default of s2_k3 is invalid')
        # Up to now not persistent
        self.assertEqual(os.path.exists(MDOtest.testConfigfile), False, ('Config file [%s] already exists.', '{}'.format(MDOtest.testConfigfile)))
        # Save
        self.assertEqual(sut.save(), True, ('Config file [%s] not saved.', '{}'.format(MDOtest.testConfigfile)))
        # Configfile must exists
        self.assertEqual(os.path.exists(MDOtest.testConfigfile), True, ('Config file [%s] missing.', '{}'.format(MDOtest.testConfigfile)))

    def test_05_load_implizit(self: object):
        """ Implizit load of config
        """
        # Configfile must exists
        self.assertEqual(os.path.exists(MDOtest.testConfigfile), True, ('Config file [%s] missing.', '{}'.format(MDOtest.testConfigfile)))
        # Init now from config file
        sut: dataTest = dataTest(MDOtest.testConfigfile)
        # Property 1
        self.assertEqual(hasattr(sut, 's1_k1'), True, 'Property s1_k1 does not exist')
        self.assertEqual('v1' == sut.s1_k1, True, 'Default of s1_k1 is invalid')
        # Property 2
        self.assertEqual(hasattr(sut, 's1_k2'), True, 'Property s1_k2 does not exist')
        self.assertEqual(42 == sut.s1_k2, True, 'Default of s1_k2 is invalid')
        # Property 3
        self.assertEqual(hasattr(sut, 's2_k3'), True, 'Property s2_k3 does not exist')
        self.assertEqual(42 == sut.s2_k3, True, 'Default of s2_k3 is invalid')

    @classmethod
    def tearDownClass(cls):
        # Ensure existing config file is removed
        if os.path.exists(MDOtest.testConfigfile):
            os.remove(MDOtest.testConfigfile)
