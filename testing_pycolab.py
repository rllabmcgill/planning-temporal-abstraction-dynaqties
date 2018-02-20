# Import necessary packages
import sys

from pycolab import ascii_art
from pycolab import human_ui
from pycolab.prefab_parts import sprites as prefab_sprites
from pycolab.rendering import ObservationToFeatureArray
import numpy as np

BLOCKING_MAZE =['###########',
				'#        G#',
				'#         #',
				'#         #',
				'######### #',
				'#         #',
				'#   S     #',
				'###########']	

SHORTCUT_MAZE = ['###########',
				 '#        G#',
				 '#         #',
				 '#         #',
				 '# #########',
				 '#         #',
				 '#   S     #',
				 '###########']	


def make_game():
	"""Builds and returns a four-rooms game."""
	return ascii_art.ascii_art_to_game(
		BLOCKING_MAZE, what_lies_beneath=' ',
		sprites={'P': PlayerSprite})

# obs, reward, gamma = game.its_showtime();
# obs, reward, gamma = game.play(1)
# state = np.array(obs.layers['P'], dtype=np.float).flatten()
# print(state)


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

	# See if we've found the mystery spot.
	if self.position == (4, 3):
		the_plot.add_reward(1.0)
		the_plot.terminate_episode()

def main(argv=()):
  del argv  # Unused.

  # Build gridworld
  game = make_game()

  # Make a CursesUi to play it with.
  ui = human_ui.CursesUi(
	  keys_to_actions={curses.KEY_UP: 0, curses.KEY_DOWN: 1,
					   curses.KEY_LEFT: 2, curses.KEY_RIGHT: 3,
					   -1: 4},
	  delay=200)

  # Let the game begin!
  ui.play(game)


if __name__ == '__main__':
  main(sys.argv)
