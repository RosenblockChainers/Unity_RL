import tensorflow as tf

from common.rl_utils import run_episode
from common.save_utils import load_model
from models.non_stochastic_policy.linear_net import LinearNet
from unityagents import UnityEnvironment


class Tester(object):
    def __init__(self, args):
        # initialize environment
        # strip out executable extensions if passed
        env_path = (args.env_name.strip()
                    .replace('.app', '')
                    .replace('.exe', '')
                    .replace('.x86_64', '')
                    .replace('.x86', ''))
        # initialize environment
        self.env = UnityEnvironment(file_name=env_path)
        print(self.env)
        # set default brain
        self.default_brain = self.env.brain_names[0]
        self.brain = self.env.brains[self.default_brain]
        # initialize model
        self.model = LinearNet(self.brain.vector_observation_space_size)
        # restore session
        self.sess = tf.InteractiveSession()
        load_model('./models/{run_id}'.format(run_id=args.run_id))

    def test(self):
        total_reward, total_step = run_episode(self.env, self.model,
                                               self.default_brain, False)
        print('total_reward: {total_reward}, total_step: {total_step}'
              .format(total_reward=total_reward, total_step=total_step))
