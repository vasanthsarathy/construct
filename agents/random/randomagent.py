from agents.agent import Agent

class RandomAgent(Agent):
    """
    Random agents
    """

    def __init__(self, ctx):
        super().__init__()
        self.config = ctx
        self.env = self.config['env']
        print("🎲 Random agent initialized.")

    def _solve(self):
        print("Solving...")
        return {'plan':[], "status":"fail"}
