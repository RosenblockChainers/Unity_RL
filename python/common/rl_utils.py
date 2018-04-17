# run one episode using policy model
def run_episode(env, model, brain_index, train_mode=True):
    # observe state of environment
    info = env.reset(train_mode=train_mode)[brain_index]
    # total reward in episode
    total_reward = 0
    # total step in episode
    episode_len = 0
    # run episode
    while True:
        # determine action using observation and model
        action = model.take_action(info)
        # perform action
        info = env.step(action)[brain_index]
        reward = info.rewards[0]
        done = info.local_done[0]
        # update total reward
        total_reward += reward
        # update total step
        episode_len += 1
        if done:
            break
    return total_reward, episode_len


# evaluate model by running episode multiple times
def evaluate_model(env, model, eval_epi, brain_index):
    # total reward
    total_reward = 0
    # total step
    step = 0
    # evaluate model
    for _ in range(eval_epi):
        r, episode_len = run_episode(env, model, brain_index)
        total_reward += r
        step += episode_len
    return total_reward / eval_epi, step
