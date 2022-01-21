from construct.planners.planner import Planner
from pyperplan.planner import _ground, _search, _parse
from pyperplan.search.breadth_first_search import breadth_first_search
import click
import subprocess
import os

class FFPlanner(Planner):
    """
    FF Planner
    """

    def __init__(self, ctx):
        super().__init__()
        self.config = ctx

    def _plan(self, domain_file, problem_file):
        output = subprocess.run(['../FF-v2.3/ff','-o', domain_file, '-f', problem_file], capture_output=True, text=True)

        plan = self._get_plan_from_stdout(output.stdout)

        click.secho(f"\tPlan: {plan}", fg="green")
        return plan

    def _get_plan_from_stdout(self,output):
        output_lst = output.split("\n")
        actions = []
        flag = False
        for line in output_lst:
            if line == "":
                flag = False
            if "step" in line:
                flag =True
            if flag:
                actions.append(line)

        actions_clean = self._clean_actions(actions)
        return actions_clean

    def _clean_actions(self,actions):
        clean = []
        for action in actions:
            if not ":" in action:
                continue
            core = action.split(":")[1].strip().lower()
            action = "("+core+")"
            clean.append(action)
        return clean


