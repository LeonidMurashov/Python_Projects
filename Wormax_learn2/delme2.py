
import gym
env = gym.make('Hopper-v1')
env.reset()
for _ in range(1000):
	env.render()
	a = env.step(env.action_space.sample()) # take a random action
	print(a)