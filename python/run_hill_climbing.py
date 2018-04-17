import argparse

from hill_climbing.trainer import Trainer
from common.tester import Tester


def main():
    parser = argparse.ArgumentParser(description='Hill Climbing')

    # setting of environment
    parser.add_argument('env_name', action='store', nargs=None,
                        help='Environment name')

    # setting of hill-climbing
    parser.add_argument('--max_episode', default=10000, type=int,
                        help='Number of episode to finish learning.')
    parser.add_argument('--eval_epi', default=5, type=int,
                        help='Number of episodes per evaluation')
    parser.add_argument('--eval_threshold', default=501, type=int,
                        help='Evaluation value as a success condition')
    parser.add_argument('--noise_scaling', default=0.25, type=float,
                        help='Scale of noise')
    parser.add_argument('--mean_init', default=-0.0, type=float,
                        help='Initial value of mean value')

    # setting of training
    parser.add_argument('--train', action='store_true', help='Whether to train')
    parser.set_defaults(test=False)
    parser.add_argument('--run_id', default='hill_climbing', type=str,
                        help='The sub-directory name for'
                             'model and summary statistics.')
    parser.add_argument('--save_model_freq', type=int, default=100,
                        help='Frequency (measured in the number of '
                             'iteration) with which the model is saved.')
    parser.add_argument('--save_summary_freq', type=int, default=1,
                        help='Frequency (measured in the number of '
                             'iteration) with which the summary is saved.')

    args = parser.parse_args()

    # run train or test
    if args.train:
        trainer = Trainer(args)
        trainer.train()
    else:
        tester = Tester(args)
        tester.test()


if __name__ == '__main__':
    main()
