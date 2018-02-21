import json
import mazes
import curses
import sys, os
import argparse
import numpy as np
from math import sqrt
import myhuman_ui as human_ui
import matplotlib.pyplot as plt


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
def eps_greedy(S, Q, eps, rnd1, rnd2, rnd4):

	uni_rnd = rnd1.uniform(0.0,1.0)
	if uni_rnd > eps:
		# check for highest Q
		# Break ties with coin flip
		action = rnd4.choice(np.flatnonzero(Q[S,:] == Q[S,:].max()))
		# action = Q[S,:].argmax()
	else:
		# choose from our 4 different possible actions randomly:
		action = rnd2.randint(0,4,1)[0]

	return action

def parse_obs(obs):

	state_mtx = np.array(obs.layers['P'], dtype=np.float)
	state_mtx = state_mtx[1:7,1:10].flatten()

	return state_mtx.argmax()


def setup_maze(maze_type, start_row, start_col):
	if maze_type == "shortcut":
		maze_init = mazes.make_maze(SHORTCUT_MAZE_INIT)
		maze_update = mazes.make_maze(SHORTCUT_MAZE_UPDATE)

	elif maze_type == "blocking":
		maze_init = mazes.make_maze(BLOCKING_MAZE_INIT)
		maze_update = mazes.make_maze(BLOCKING_MAZE_UPDATE)


	# Place engines in play mode
	maze_init.its_showtime()
	maze_update.its_showtime()

	# Move agent to starting position
	maze_init._sprites_and_drapes['P']._teleport((start_row, start_col))
	maze_update._sprites_and_drapes['P']._teleport((start_row, start_col))

	return maze_init, maze_update


def run_experiment(config_file_path):

	if not os.path.exists(config_file_path): raise argparse.ArgumentTypeError('Not a valid config file')

	with open(config_file_path, 'r') as config_fd:
		config = json.load(config_fd)

	# Initializations
	terminal_steps = config['terminal_steps']
	switch_steps = config['switch_maze_at_step']

	maze_type = config['maze_type']
	arch = config['arch']
	nrow = config['maze_params']['row']
	ncol = config['maze_params']['col']
	start_row = config['maze_params']['start_row']
	start_col = config['maze_params']['start_col']

	eps = config['policy_params']['epsilon']
	alpha = config['learning_alg_params']['alpha']
	gamma = config['learning_alg_params']['gamma']
	kappa = config['planner_params']['kappa']
	sim_epoch = config['model_params']['sim_epoch']


	state_len = nrow*ncol
	action_len = 4
	reward_len = 2

	# Don't need all these guys
	rnd1 = np.random.RandomState(24)
	rnd2 = np.random.RandomState(42)
	rnd3 = np.random.RandomState(57)
	rnd4 = np.random.RandomState(13)
	rnd5 = np.random.RandomState(66)

	# Check for algo
	if arch == 'dyna_q':
		model = dict()
	elif arch == 'dyna_q_plus':
		visited_step = dict()
		model = dict()
		for s in range(0,state_len):
			for a in range(0, 4):
				model[(s,a)] = (s,0)
				visited_step[(s,a)] = 0

	Q = np.zeros((state_len, action_len))

	# Starting position of our agent

	steps = 0
	episodes = 0
	cum_reward = 0
	cum_reward_lst = []

	S = xy2flat(start_row, start_col)
	S_prime = S

	# Initialize maze
	maze_init, maze_update = setup_maze(maze_type, start_row, start_col)
	curr_maze = maze_init

	while steps <= terminal_steps:

		# Reset episode:
		if curr_maze._game_over:
			S = xy2flat(start_row, start_col)
			S_prime = S
			maze_init, maze_update = setup_maze(maze_type, start_row, start_col)
			print("New episode starting...")
			print("Current step: " + str(steps))
			print("Agent's position: " + str(maze_init._sprites_and_drapes['P']._virtual_row) + ", " + str(maze_init._sprites_and_drapes['P']._virtual_col))
			curr_maze = maze_init # only doing this to reset the agent to the starting position, the next if statement will actually correct the map if need be

			episodes += 1

		# The maze evolves after switch_steps:
		if steps <= switch_steps:
			curr_maze = maze_init
		else:
			old_row, old_col = curr_maze._sprites_and_drapes['P']._virtual_row, \
							   curr_maze._sprites_and_drapes['P']._virtual_col
			
			# If agent happens to be where a new wall is added by the environment changing
			# Move the agent to an open location randomly (either up one row or down one row)
			if old_row == 4 and old_col == 9:
				if rnd5.randint(0,2) == 1:
					old_row += 1
					S_prime += 9
				else:
					old_row -= 1
					S_prime -= 9
				maze_update._sprites_and_drapes['P']._teleport((old_row, old_col))
			else:
				maze_update._sprites_and_drapes['P']._teleport((old_row, old_col))
			curr_maze = maze_update

		# Get current state S
		S = S_prime

		# Select Action A using epsilon-greedy (given S, Q)
		A = eps_greedy(S, Q, eps, rnd1, rnd2, rnd4)
		# print("Action is: " + str(A))




		# Apply action A to current maze, get reward R, and new state S'
		obs, R, _ = curr_maze.play(A)
		S_prime = parse_obs(obs)

		# Update Q function
		Q[S,A] = Q[S,A] + alpha*( R + gamma*Q[S_prime,:].max() - Q[S,A] )

		# print("Reward R is: " + str(R))

		# Update Model with R, S_prime for a particular state action pair
		model[(S,A)] = (R, S_prime)

		# Dyna-Q+ only
		if arch == 'dyna_q_plus':
			visited_step[(S,A)] = steps

		# Loop sim_epoch times (simulation):
		for i in range(sim_epoch):
			# Get random previously observed state S
			# Get random previously taken action A for that state S
			rnd_S, rnd_A = model.keys()[ rnd3.randint(0, len(model), 1)[0] ]

			# Extract reward R and next state S' for that action A from Model
			sim_R, sim_S_prime = model[(rnd_S, rnd_A)]

			if arch == 'dyna_q_plus':
				tau = steps - visited_step[(rnd_S, rnd_A)] 
				sim_R += kappa*sqrt(tau)			

			# Update Q function
			Q[rnd_S, rnd_A] = Q[rnd_S,rnd_A] + alpha*( sim_R + gamma*Q[sim_S_prime,:].max() - Q[rnd_S, rnd_A] )

		# print("Current step: " + str(steps))
		cum_reward += R
		cum_reward_lst.append(cum_reward)
		steps += 1

	print("Number of episodes completed: " + str(episodes))
	print("Cumulative reward: " + str(cum_reward))
	plt.plot(range(0,steps), cum_reward_lst)
	plt.ylabel('Cumulative Rewards')
	plt.xlabel('Number of steps')
	plt.show()

def main(argv):

	parser = argparse.ArgumentParser()
	parser.add_argument('config_file', type=str,  help="Configuration file path. e.g. blocking.config")
	args = parser.parse_args()

	#Reading config file
	config_file_path = args.config_file

	run_experiment(config_file_path)

if __name__ == '__main__':
	main(sys.argv)
