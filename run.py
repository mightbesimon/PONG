#!/usr/bin/env python3

from game import Game


def main():
	game = Game('PONG')
	game.setup()

	while not game.over:
		game.tick()

	game.cleanup()


if __name__ == '__main__': main()

