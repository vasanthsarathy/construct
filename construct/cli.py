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
@click.option('--agent', default="random", type=click.Choice(["random", "biplex"]), help="Choose agent")
@click.option('--env', default="PDDLEnvPolycraft-v0", type=click.Choice(["PDDLEnvPolycraft-v0"]), help="Choose gym environment")
@click.option('--bias', default="agents/random/bias/polycraft_complete.pddl", help="Choose agent's domain bias file location")
@click.option('--goal', default="(have ?x-pogostick1)", help="Select goal for the agent")
@click_config_file.configuration_option(cmd_name='construct', config_file_name=os.path.join(ROOT_DIR, 'config/config_default.yml'))
@click.pass_context
def run(ctx, **kwargs):

    ctx.obj.update(kwargs)

    with open('construct/config/config_default_auto.json', 'w+') as config_dump:
        config_dump.write(json.dumps(ctx.obj))

    exp = Experiment(ctx=ctx.obj)
    exp.run_one()
    exp.show_results()


cli.add_command(run)

def main():
    cli(obj={})

if __name__ == "__main__":
    main()

