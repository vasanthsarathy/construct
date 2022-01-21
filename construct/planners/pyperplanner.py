from construct.planners.planner import Planner
from pyperplan.planner import _ground, _search, _parse
from pyperplan.search.breadth_first_search import breadth_first_search
import click

class PyperPlanner(Planner):
    """
    Pyperplan
    """

    def __init__(self, ctx):
        super().__init__()
        self.config = ctx

    def _plan(self, domain_file, problem_file):
        problem = _parse(domain_file, problem_file)
        task = _ground(problem)
        print(f"\tDomain: {domain_file}")
        print("\t*Planning*", end="\r")
        solution = breadth_first_search(task)
        solution = [x.name for x in solution]
        click.secho(f"\tPlan: {solution}", fg="green")
        return solution



