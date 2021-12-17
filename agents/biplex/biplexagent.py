from agents.agent import Agent
import pddlgym

class BiplexAgent(Agent):
    """
    Biplex
    """

    def __init__(self, ctx):
        super().__init__()
        self.config = ctx
        self.env = pddlgym.make(self.config['env'])
        self.goal = self.config['goal']
        print("🍁 Biplex agent initialized.")

    def _solve(self):
        return {'plan':[], "status":"NA"}


