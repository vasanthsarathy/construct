# cli.py

import os
import sys
import click
import click_config_file
import json

from experiments.experiment import Experiment

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Shared click options
shared_options = [
    click.option('--verbose/--no-verbose', '-v', default=False, help="If set, console output is verbose"),
    click.option('--expts_folder', default='experiments/', help="Parent folder for experiments.")
]

def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options

@click.group()
@click.option('--verbose/--no-verbose', '-v', default=False, help="If set, console output is verbose")
@click.pass_context
def cli(ctx, **kwargs):
    ctx.ensure_object(dict)
    ctx.obj = kwargs
    click.clear()
    click.secho('🛠️  Construct', fg='blue')
    click.secho(f"Constructive Problem Solving Environment", fg='yellow')
    print(f'-----------------')

@click.command()
@add_options(shared_options)
@click.option('--agent', default="biplex", type=click.Choice(["random", "biplex"]), help="Choose agent")
@click.option('--env', default="PDDLEnvTreasure-v0", type=click.Choice(["PDDLEnvPancake-v0", "PDDLEnvTreasure-v0"]), help="Choose pddlgym environment")
@click.option('--bias', default="agents/biplex/bias/treasure.pddl", help="Agent's domain bias file location")
@click.option('--resource_graph', default="agents/biplex/bias/crafting_knowledge.gml", help="Agent's resource graph knowledge")
@click.option('--goal', default="(have ?x-p)", help="Select goal for the agent")
@click.option('--planner', default="ff", help="Select agent's planner")
@click.option('--problem', default=0, help="Select problem number. Tied to env.")
@click_config_file.configuration_option(cmd_name='construct', config_file_name=os.path.join(ROOT_DIR, 'config/config_default.yml'))
@click.pass_context
def run(ctx, **kwargs):

    ctx.obj.update(kwargs)

    with open('construct/config/config_default_auto.json', 'w+') as config_dump:
        config_dump.write(json.dumps(ctx.obj))

    exp = Experiment(ctx=ctx.obj)
    exp.run_one()
    # exp.show_results()


cli.add_command(run)

def main():
    cli(obj={})

if __name__ == "__main__":
    main()
