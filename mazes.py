# Import necessary packages
import sys

from pycolab import ascii_art
# from pycolab import human_ui
from pycolab.prefab_parts import sprites as prefab_sprites
from pycolab.rendering import ObservationToFeatureArray
import numpy as np
import curses


						 


def make_maze(maze):
	"""Builds and returns a blocking maze gridworld game."""
	return ascii_art.ascii_art_to_game(
		maze, what_lies_beneath=' ',
		sprites={'S': PlayerSprite})

# Epsilon-greedy implementation for choosing next action
# def choose_next_action(state, ):


class PlayerSprite(prefab_sprites.MazeWalker):
	"""A `Sprite` for our player.

	This `Sprite` ties actions to going in the four cardinal directions. If we
	reach a magical location (in this example, (4, 3)), the agent receives a
	reward of 1 and the epsiode terminates.
	"""

	def __init__(self, corner, position, character):
		"""Inform superclass that we can't walk through walls."""
		super(PlayerSprite, self).__init__(
			corner, position, character, impassable='#')

	def update(self, actions, board, layers, backdrop, things, the_plot):
		del layers, backdrop, things   # Unused.

		# Apply motion commands.
		if actions == 0:    # walk upward?
			self._north(board, the_plot)
		elif actions == 1:  # walk downward?
			self._south(board, the_plot)
		elif actions == 2:  # walk leftward?
			self._west(board, the_plot)
		elif actions == 3:  # walk rightward?
			self._east(board, the_plot)

		# See if we've found the goal:
		if self.position == (1, 9):
			the_plot.add_reward(1.0)
			the_plot.terminate_episode()


