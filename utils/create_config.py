import json

config = {'arch' : 'dyna_q_plus',
          'terminal_step' : 6000,
          'switch_maze_at_step' : 2000,
          'maze_type' : 'blocking',
          'maze_params' : {
              'row' : 6,
              'col' : 9,
              'start_row' : 6,
              'start_col' : 4
          },
          'policy' : 'epsilon_greedy',
          'policy_params' : {
              'epsilon' : 0.1,
              'seed' : 24
          },
          'learning_alg' : 'q_learning',
          'learning_alg_params' : {
              'alpha' : 0.1,
              'gamma' : 0.95,
              'seed' : 42
          },
          'model' : 'deterministic_no_prior',
          'model_params' : {
              'sim_epoch' : 50
          },
          'planner_params' : {
              'kappa' : 0.01
          }
         }

filename = "../config/blocking.config"
with open(filename, 'w') as fd:
    json.dump(config, fd)
