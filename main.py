import argparse
import pygame
import time

from ConfigParser import SafeConfigParser

from ocean import configurations
from ocean import Ocean


def run_visualization(ocean_config, display_config, ocean, output_filename):
    pygame.init()

    screen = pygame.display.set_mode(display_config.window_parameters)
    pygame.display.set_caption(display_config.version)
    background = pygame.Surface(display_config.window_parameters)
    background.fill(pygame.Color(display_config.background_color))

    for iteration in xrange(display_config.iterations):
        if ocean.is_over:
            break

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                ocean.to_file(output_filename)
                raise SystemExit, "Quit. Bye-bye :)"

        ocean.make_one_iteration(iteration)

        corner_x = 0
        corner_y = 0
        for i in xrange(ocean_config.size_ocean):
            for j in xrange(ocean_config.size_ocean):
                label = ocean.ocean[i][j]
                cell_color = display_config.colors[label]

                cell = pygame.Surface(display_config.cell_parameters)
                cell.fill(pygame.Color(cell_color))
                screen.blit(cell, (corner_x, corner_y))

                corner_x += display_config.cell_size
            corner_y += display_config.cell_size
            corner_x = 0

        pygame.display.update()
        time.sleep(display_config.time_sleep)


def random_ocean(args):
    config_parser = SafeConfigParser()
    config_parser.read(args.configuration)

    ocean_config = configurations.OceanRandomConfig(config_parser)
    display_config = configurations.DisplayBaseConfig(config_parser, args.iterations)
    
    ocean = Ocean(ocean_config)
    ocean.initialize_random()

    run_visualization(ocean_config, display_config, ocean, args.output)

    ocean.to_file(args.output)


def from_file_ocean(args):
    config_parser = SafeConfigParser()
    config_parser.read(args.configuration)

    ocean_config = configurations.OceanFileConfig(config_parser)
    display_config = configurations.DisplayBaseConfig(config_parser, args.iterations)
    
    ocean = Ocean(ocean_config)
    ocean.initialize_from_file(args.input)

    run_visualization(ocean_config, display_config, ocean, args.output)

    ocean.to_file(args.output)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-i', '--iterations', type=int, default=1000)
    arg_parser.add_argument('-c', '--configuration', type=str)
    arg_parser.add_argument('-o', '--output', type=str)

    subparsers = arg_parser.add_subparsers()

    random_parser = subparsers.add_parser('random')
    random_parser.set_defaults(which='random', func=random_ocean)

    file_parser = subparsers.add_parser('from_file')
    file_parser.add_argument('-in', '--input', type=str)
    file_parser.set_defaults(which='from_file', func=from_file_ocean)
    
    args = arg_parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
