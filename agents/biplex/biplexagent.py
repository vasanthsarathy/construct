from agents.agent import Agent
import pddlgym
import networkx as nx
from construct.wrappers import PyperWrapper
from pyperplan.pddl.pddl import Type, Problem, Predicate
from pyperplan.pddl.parser import Parser
from pyperplan.planner import _ground, _search, _parse
from pyperplan.grounding import ground
from pyperplan.search.breadth_first_search import breadth_first_search
import random
import uuid
import copy

# UPDATED to produce problem.pddl files instead of dealing with generating predicates etc.


class BiplexAgent(Agent):
    """
    Biplex
    """

    def __init__(self, ctx):
        super().__init__()
        self.config = ctx
        self.env = PyperWrapper(pddlgym.make(self.config['env']))
        self.env.reset()
        self.goal = self.config['goal']
        # self.trees = self._parse_trees_file(self.config['trees'])
        print("🍁 Biplex agent initialized.")

    def _solve(self):
        status, s1 = self.prove()
        if status:
            return {'plan':[], 'final_state':s1, "status":status}
        return {'plan':[], 'final_state':s1, "status":False}

    def prove(self):
        status, s1 = self.plan_execute()
        print(status, s1)
        return False, []

    def plan_execute(self):
        """
        goal = lifted  or grounded
        assume that we only have one predicate
        """
        # Update goal by grounding it either with something in the environment or with a hypo
        self.goal = self._ground_goal(self.config['goal'])
        # Create a problem_file
        goal_line = f"(:goal {self.goal})"
        init_line = "(:init" + " " + " ".join(set(self.env.observe())) + ")"
        objects = []
        for k,v in self.env.objects().items():
            objects.append(f"{k} - {v}")
        objects_line = "(:objects" + " " + " ".join(objects) + ")"
        domain_line = "(:domain treasure)" #HACK TODO need to fix
        define_line = "(define (problem treasure)" #HACK TODO fix
        # Generate problem instance from domain and problem file

        self.problem_file = "agents/biplex/temp/problem_gen.pddl"
        with open(self.problem_file, "w+") as f:
            f.write(define_line)
            f.write("\n\n")
            f.write(domain_line)
            f.write("\n\n")
            f.write(objects_line)
            f.write("\n\n")
            f.write(init_line)
            f.write("\n\n")
            f.write(goal_line)
            f.write("\n\n")
            f.write(")")

        # Generate task and run search
        problem = _parse(self.config['bias'], self.problem_file)
        task = _ground(problem)
        print("planning...")
        solution = breadth_first_search(task)
        print(solution)


        return False, []

    def _ground_goal(self, atom_str):
        """
        Given an atom (have ?x-t) or (have t23) or (on ?x-t y24-y)  or (have ?t34-t)
        Return (have t23)
        """

        objs = self.env.objects()  # CHANGE TO SELF.ENV
        type_keyed_objs = {}
        for k,v in objs.items():
            type_keyed_objs[v.name]= type_keyed_objs.get(v.name,[])
            type_keyed_objs[v.name].append(k)

        name = atom_str.replace("(","").replace(")","").split(" ")[0]
        args = atom_str.replace("(","").replace(")","").split(" ")[1:]
        new_args = []
        for arg in args:
            if "?" in arg:
                if "-" in arg:
                    typing = arg.split("-")[1]
                    if typing in type_keyed_objs:
                        # Assign random name
                        new_sym = random.choice(type_keyed_objs[typing])
                        new_args.append(f"{new_sym}")
                    else:
                        # Assign hypothetical name
                        hypo_sym = f"{typing}_{str(uuid.uuid4())[:8]}"
                        new_args.append(f"{hypo_sym}")
                else:
                    raise ValueError("Must provide at least one of constant or a type")
            else:
                if "-" in arg:
                    new_arg = arg.split("-")[0]
                    new_args.append(new_arg)
                else:
                    new_args.append(arg)
        new_atom = "("+name+" "+" ".join(new_args)+")"
        return new_atom




    def _parse_trees_file(self, trees_file):
        trees = []
        # TODO: load file, generate a list of networkx trees
        return trees

