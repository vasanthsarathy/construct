from agents.agent import Agent
import pddlgym
from construct.wrappers import StringWrapper

class RandomAgent(Agent):
    """
    Random agents
    """

    def __init__(self, ctx):
        super().__init__()
        self.config = ctx
        self.env = StringWrapper(pddlgym.make(self.config['env']))
        self.goal = self.config['goal']
        print("🎲 Random agent initialized.")

    def _solve(self):
        print("Solving...")
        obs, _ = self.env.reset()
        print(f"Initial State:\n {obs}")
        print("-------------")
        action_str = "move(tree1_7:tree1, crafting_table1_5:crafting_table1)"
        obs, _, _, _ = self.env.step(action_str)
        print("-------------")
        print(f"Final State: \n {obs}")
        return {'plan':action_str, "status":"completed"}


