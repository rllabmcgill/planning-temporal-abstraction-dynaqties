import sys
import mazes
import curses
import argparse
import numpy as np
import myhuman_ui as human_ui

BLOCKING_MAZE_INIT =['###########',
					 '#        G#',
					 '#         #',
					 '#         #',
					 '######### #',
					 '#         #',
					 '#   P     #',
					 '###########']	

BLOCKING_MAZE_UPDATE =  ['###########',
						 '#        G#',
						 '#         #',
						 '#         #',
						 '# #########',
						 '#         #',
						 '#   P     #',
						 '###########']	

SHORTCUT_MAZE_INIT   =  ['###########',
						 '#        G#',
						 '#         #',
						 '#         #',
						 '# #########',
						 '#         #',
						 '#   P     #',
						 '###########']	

SHORTCUT_MAZE_UPDATE =['###########',
					   '#        G#',
					   '#         #',
					   '#         #',
					   '# ####### #',
					   '#         #',
					   '#   P     #',
					   '###########']	

nrow = 6
ncol = 9

def flat2xy(f):
	f = f + 1 # f indexes from 0, gridworld indexes from 1
	y = f%ncol
	x = (f-y)/ncol + 1
	return x, y

def xy2flat(x,y):
	f = (x-1)*9+y
	f = f - 1 # f indexes from 0, gridworld indexes from 1
	return f

# e-greedy algorithm for choosing next action
def eps_greedy(S, Q, eps, rnd1, rnd2):

	uni_rnd = rnd1.uniform(0.0,1.0)
	if uni_rnd > eps:
		# check for highest Q
		# TODO: break ties with coin flip
		action = Q[S,:].argmax()

	else:
		# choose from our 4 different possible actions randomly:
		
		action = rnd2.randint(0,4,1)[0]
	
	return action

def parse_obs(obs):

	state_mtx = np.array(obs.layers['P'], dtype=np.float)
	state_mtx = state_mtx[1:7,1:10].flatten()

	return state_mtx.argmax()

def main(argv=()):

	parser = argparse.ArgumentParser()
	parser.add_argument('world', type=str, help="Type of gridworld.", choices=["blocking", "shortcut"])
	args = parser.parse_args()
	maze_type = args.world

	if maze_type == "shortcut":
		maze_init = mazes.make_maze(SHORTCUT_MAZE_INIT)
		maze_update = mazes.make_maze(SHORTCUT_MAZE_UPDATE)

	elif maze_type == "blocking":
		maze_init = mazes.make_maze(BLOCKING_MAZE_INIT)
		maze_update = mazes.make_maze(BLOCKING_MAZE_UPDATE)


	# episodes = 0
	terminal_steps = 1000
	switch_steps = 50

	# Initializations of Q, model, alpha, epsilon, gamma, sim_epoch (ie: n), random_seed

	eps = 0.1
	alpha = 0.1
	gamma = 0.95
	sim_epoch = 5

	state_len = nrow*ncol
	action_len = 4
	reward_len = 2
	start_row = 6
	start_col = 4

	rnd1 = np.random.RandomState(24)
	rnd2 = np.random.RandomState(42)

	model = dict()
	Q = np.zeros((state_len, action_len))


	maze_init._sprites_and_drapes['P']._teleport((start_row, start_col))
	S = xy2flat(start_row, start_col)
	S_prime = S

	steps = 0

	# Place engines in play mode
	maze_init.its_showtime()
	maze_update.its_showtime()

	while steps <= terminal_steps:

		if steps <= 50:
			curr_maze = maze_init
		else:
			# TODO: weird model update wall situation

			old_row, old_col = curr_maze._sprites_and_drapes['P']._virtual_row, \
							   curr_maze._sprites_and_drapes['P']._virtual_col
			maze_update._sprites_and_drapes['P']._teleport((old_row, old_col))
			curr_maze = maze_update

		# Get current state S
		S = S_prime	

		# Select Action A using epsilon-greedy (given S, Q)
		A = eps_greedy(S, Q, eps, rnd1, rnd2)
		print("Action is: " + str(A))

		# Apply action A to current maze, get reward R, and new state S'
		obs, R, _ = curr_maze.play(A)
		S_prime = parse_obs(obs)

		# Update Q function
		Q[S,A] = Q[S,A] + alpha*( R + gamma*Q[S_prime,:].max() - Q[S,A] )

		# Update Model


		# Loop sim_epoch times (simulation):

			# Get random previously observed state S

			# Get random previously taken action A for that state S

			# Extract reward R and next state S' for that action A from Model

			# Update Q function

		steps += 1


	# Make a CursesUi to play it with.
	# ui = human_ui.CursesUi(
	# 	 keys_to_actions={curses.KEY_UP: 0, curses.KEY_DOWN: 1,
	# 					   curses.KEY_LEFT: 2, curses.KEY_RIGHT: 3,
	# 					   -1: 4},
	# 	 delay=200)

	# ui.play(maze_init, maze_update)


if __name__ == '__main__':
	main(sys.argv)
