import unittest

from ConfigParser import SafeConfigParser

from ocean import creatures
from ocean import configurations 
from ocean import Ocean


class TestVictimMethods(unittest.TestCase):
    def setUp(self):
        self.duration_life = 100
        self.reproduction = 20
        self.size_ocean = 50
        
        filename = 'ocean.config'
        config_parser = SafeConfigParser()
        config_parser.read(filename)

        self.ocean_config = configurations.OceanBaseConfig(config_parser)
        self.ocean = Ocean(self.ocean_config)
        self.ocean.create_empty()

    def test_reproduction(self):
        victim = creatures.Victim(45, 45, self.duration_life)
        self.ocean.ocean[45][45] = self.ocean_config.label_victim
        self.ocean.victims.append(victim)

        self.ocean.victim_reproduction()

        self.assertEqual(self.ocean.ocean[victim.get_x()][victim.get_y()], self.ocean_config.label_victim)

        child = False
        for i in xrange(len(self.ocean_config.dx)):
            x_new = victim.get_x() + self.ocean_config.dx[i]
            y_new = victim.get_y() + self.ocean_config.dy[i]
            if self.ocean.ocean[x_new][y_new] == self.ocean_config.label_victim:
                child = True
        self.assertTrue(child, True)

    def test_moving(self):
        victim = creatures.Victim(20, 20, self.duration_life)
        self.ocean.ocean[20][20] = self.ocean_config.label_victim
        self.ocean.victims.append(victim)
        pref_x = victim.get_x()
        pref_y = victim.get_y()

        self.ocean.step_victim(victim)
        new_x = victim.get_x()
        new_y = victim.get_y()

        self.assertEqual(self.ocean.ocean[new_x][new_y], self.ocean_config.label_victim)
        self.assertEqual(self.ocean.ocean[pref_x][pref_y], self.ocean_config.label_empty)
        self.assertNotEqual([new_x, new_y], [pref_x, pref_y])


if __name__ == '__main__':
    unittest.main()
