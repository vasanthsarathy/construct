from agents.random.randomagent import RandomAgent
from agents.biplex.biplexagent import BiplexAgent

class Experiment:

    def __init__(self, ctx):
        self.config = ctx
        self.agent = self.config['agent']
        self.env = self.config['env']
        self.goal = self.config['goal']
        self.bias = self.config['bias']
        self.solution = {}

    def run_one(self):
        agent = None
        if self.agent == "random":
            agent = RandomAgent(self.config)
        elif self.agent == "biplex":
            agent = BiplexAgent(self.config)
        if agent:
            self.solution = agent.solve()
            return
        print("Error initializing and running agent")
        return


    def show_results(self):
        print(f"showing results: {self.solution}")
        pass


