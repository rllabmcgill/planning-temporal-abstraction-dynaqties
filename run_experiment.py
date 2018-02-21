import sys


import mazes
import curses
import myhuman_ui as human_ui

BLOCKING_MAZE_INIT =['###########',
					 '#        G#',
					 '#         #',
					 '#         #',
					 '######### #',
					 '#         #',
					 '#   S     #',
					 '###########']	

BLOCKING_MAZE_UPDATE =  ['###########',
						 '#        G#',
						 '#         #',
						 '#         #',
						 '# #########',
						 '#         #',
						 '#   S     #',
						 '###########']	

STOPPING_MAZE_INIT   =  ['###########',
						 '#        G#',
						 '#         #',
						 '#         #',
						 '# #########',
						 '#         #',
						 '#   S     #',
						 '###########']	

STOPPING_MAZE_UPDATE =['###########',
					   '#        G#',
					   '#         #',
					   '#         #',
					   '# ####### #',
					   '#         #',
					   '#   S     #',
					   '###########']	


def main(argv=()):
	del argv  # Unused.

	episodes = 0
	steps = 0

	# Build gridworld
	maze_init = mazes.make_maze(BLOCKING_MAZE_INIT)
	maze_update = mazes.make_maze(BLOCKING_MAZE_UPDATE)

	# Make a CursesUi to play it with.
	ui = human_ui.CursesUi(
		 keys_to_actions={curses.KEY_UP: 0, curses.KEY_DOWN: 1,
						   curses.KEY_LEFT: 2, curses.KEY_RIGHT: 3,
						   -1: 4},
		 delay=200)

	ui.play(maze_init, maze_update)


if __name__ == '__main__':
	main(sys.argv)
