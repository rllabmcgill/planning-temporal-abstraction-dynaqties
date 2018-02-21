import json

config = {'terminal_steps' : 6000,
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
              'seed' : 10
          },
          'learning_alg' : 'q_learning',
          'learning_alg_params' : {
              'alpha' : 0.1,
              'gamma' : 0.95,
              'seed' : 10
          },
          'model' : 'deterministic_no_prior',
          'model_params' : {
              'sim_epoch' : 5
          }
         }

filename = "blocking.config"
with open(filename, 'w') as fd:
    json.dump(config, fd)
