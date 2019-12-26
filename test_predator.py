import unittest

from ConfigParser import SafeConfigParser

from ocean import creatures
from ocean import configurations 
from ocean import Ocean


class TestPredatorMethods(unittest.TestCase):
    def setUp(self):
        self.duration_life = 15
        self.reproduction = 14
        self.satiety = 3
        self.size_ocean = 50
        
        filename = 'ocean.config'
        config_parser = SafeConfigParser()
        config_parser.read(filename)

        self.ocean_config = configurations.OceanBaseConfig(config_parser)
        self.ocean = Ocean(self.ocean_config)
        self.ocean.create_empty()

    def test_reproduction(self):
        predator = creatures.Predator(48, 48, self.satiety, self.duration_life)
        self.ocean.ocean[48][48] = self.ocean_config.label_predator
        self.ocean.predators.append(predator)

        self.ocean.predator_reproduction()
        self.assertEqual(self.ocean.ocean[predator.get_x()][predator.get_y()], self.ocean_config.label_predator)

        child = False
        for i in xrange(len(self.ocean_config.dx)):
            x_new = predator.get_x() + self.ocean_config.dx[i]
            y_new = predator.get_y() + self.ocean_config.dy[i]
            if self.ocean.ocean[x_new][y_new] == self.ocean_config.label_predator:
                child = True
        self.assertTrue(child, True)

    def test_moving(self):
        predator = creatures.Predator(1, 1, self.satiety, self.duration_life)
        self.ocean.ocean[1][1] = self.ocean_config.label_predator
        pref_x = predator.get_x()
        pref_y = predator.get_y()

        self.ocean.step_predator(predator)
        new_x = predator.get_x()
        new_y = predator.get_y()
        
        self.assertEqual(self.ocean.ocean[pref_x][pref_y], self.ocean_config.label_empty)
        self.assertEqual(self.ocean.ocean[new_x][new_y], self.ocean_config.label_predator)
        self.assertNotEqual([new_x, new_y], [pref_x, pref_y])

    def test_eating(self):
        predator = creatures.Predator(25, 25, self.satiety, self.duration_life)
        self.ocean.ocean[25][25] = self.ocean_config.label_predator
        pref_x = predator.get_x()
        pref_y = predator.get_y()

        victim = creatures.Victim(26, 25, 10)
        self.ocean.ocean[26][25] = self.ocean_config.label_victim
        vict_x = victim.get_x()
        vict_y = victim.get_y()

        self.ocean.step_predator(predator)

        self.assertEqual(self.ocean.ocean[pref_x][pref_y], self.ocean_config.label_empty)
        self.assertEqual([predator.get_x(), predator.get_y()], [vict_x, vict_y])
        self.assertEqual(self.ocean.ocean[vict_x][vict_y], self.ocean_config.label_predator)


if __name__ == '__main__':
    unittest.main()
