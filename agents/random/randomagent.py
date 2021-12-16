from agents.agent import Agent
import pddlgym

class RandomAgent(Agent):
    """
    Random agents
    """

    def __init__(self, ctx):
        super().__init__()
        self.config = ctx
        self.env = pddlgym.make(self.config['env'])
        self.goal = self.config['goal']
        print("🎲 Random agent initialized.")

    def _solve(self):
        print("Solving...")
        obs, _ = self.env.reset()
        print(f"Initial State:\n {obs}")
        print("-------------")
        actions = []
        for _ in range(10):
            action = self.env.action_space.sample(obs)
            print(action)
            actions.append(action)
            obs, _, _, _ = self.env.step(action)
        print("-------------")
        print(f"Final State: \n {obs}")
        return {'plan':actions, "status":"completed"}


