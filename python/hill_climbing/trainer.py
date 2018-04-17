import os
import numpy as np
import tensorflow as tf

from common.rl_utils import evaluate_model
from common.save_utils import save_model, export_graph
from common.summarizer import Summarizer
from unityagents import UnityEnvironment
from models.non_stochastic_policy.linear_net import LinearNet


class Trainer(object):
    def __init__(self, args):
        # initialize environment
        # strip out executable extensions if passed
        env_path = (args.env_name.strip()
                    .replace('.app', '')
                    .replace('.exe', '')
                    .replace('.x86_64', '')
                    .replace('.x86', ''))
        self.env = UnityEnvironment(file_name=env_path)
        self.env_name = os.path.basename(os.path.normpath(env_path))
        print(str(self.env))

        # initialize training setting
        self.run_id = args.run_id
        self.model_path = './models/{run_id}'.format(run_id=self.run_id)
        self.save_model_freq = args.save_model_freq
        self.save_summary_freq = args.save_summary_freq

        # set default brain
        self.default_brain = self.env.brain_names[0]
        self.brain = self.env.brains[self.default_brain]
        # initialize model
        self.model = LinearNet(self.brain.vector_observation_space_size)

        # max number of episode
        self.max_episode = args.max_episode
        # number of episodes per evaluation
        self.eval_epi = args.eval_epi
        # if total reward is more than threshold, trial is regarded as a success
        self.eval_threshold = args.eval_threshold

        # parameter of hill-climbing
        self.noise_scaling = args.noise_scaling
        self.mean_init = args.mean_init

    # main loop
    def train(self):
        # initialize session
        tf.InteractiveSession()

        # initialize parameters of hill-climbing
        param_dim = self.model.param_vector().size
        best_param = np.ones((param_dim, 1)) * self.mean_init

        # best total reward in this trial
        best_total_reward = -1e10
        # number of episode
        num_epi = 0
        # total step
        step = 0

        # initialize summarizer
        summarizer = Summarizer('./summaries/' + self.run_id)

        # main loop of hill-climbing
        g = 0
        episode_len = 0
        total_reward = 0
        for g in range(int(self.max_episode / self.eval_epi)):
            # sample new parameter on the basis of the now parameter
            new_param = best_param + (
                    np.random.rand(param_dim, 1) * 2 - 1) * self.noise_scaling
            self.model.update_param(new_param)
            # evaluate new parameter
            total_reward, episode_len = evaluate_model(self.env,
                                                       self.model,
                                                       self.eval_epi,
                                                       self.default_brain)
            num_epi += self.eval_epi
            step += episode_len

            # if best total reward in this iteration
            # is more than best total reward,
            # update best total reward and now parameter
            if total_reward > best_total_reward:
                best_param = self.model.param_vector()
                best_total_reward = total_reward
                # if best total reward is more than threshold, finish trial
                if total_reward >= self.eval_threshold:
                    break

            # save model
            if g % self.save_model_freq == 0:
                save_model(self.model_path, g)
            # summarize
            if g % self.save_summary_freq == 0:
                summarizer.write({'iteration': g,
                                  'total_reward': total_reward,
                                  'best_total_reward': best_total_reward,
                                  'episode_length': episode_len / self.eval_epi,
                                  'num_episode': num_epi},
                                 step)
            # debug print
            if g % 10 == 0:
                print('iteration: {0}, '
                      'num_episode: {1}, '
                      'step: {2}, '
                      'total_reward: {3}, '
                      'best_total_reward: {4}'
                      .format(g, num_epi, step, total_reward,
                              best_total_reward))

        # finalize
        self.env.close()
        self.model.update_param(best_param)

        # save model
        save_model(self.model_path, g)
        # summarize
        summarizer.write({'total_reward': total_reward,
                          'best_total_reward': best_total_reward,
                          'episode_length': episode_len / self.eval_epi,
                          'num_episode': num_epi},
                         step)
        export_graph(self.model_path, self.env_name, self.run_id)

        # if number of episode required to solve of trial
        # is equal to max number of episode,
        # trial is regarded as a failure.
        # else,
        # trial is regarded as a success.
        is_success = num_epi != self.max_episode
        print('success: {0}, '
              'iteration: {1}, '
              'num_episode: {2}, '
              'step: {3}, '
              'best_total_reward: {4}'
              .format(is_success, g, num_epi, step, best_total_reward))
        print('best_model: {0}'.format(self.model))
