from agents.agent import Agent
import pddlgym
import networkx as nx
from construct.wrappers import PyperWrapper
from pyperplan.pddl.pddl import Type, Problem, Predicate
from pyperplan.pddl.parser import Parser
from pyperplan.planner import _ground, _search, _parse
from pyperplan.grounding import ground
from pyperplan.search.breadth_first_search import breadth_first_search
from pyperplan.search.a_star import astar_search
from pyperplan.search.a_star import greedy_best_first_search
from pyperplan.search.iterative_deepening_search import iterative_deepening_search
import random
import uuid
import copy
import networkx as nx
import click
# UPDATED to produce problem.pddl files instead of dealing with generating predicates etc.


class BiplexAgent(Agent):
    """
    Biplex
    """

    def __init__(self, ctx):
        super().__init__()
        self.config = ctx
        self.env = PyperWrapper(pddlgym.make(self.config['env']))
        self.env.fix_problem_index(1)
        self.env.reset()
        self.goal = self.config['goal']
        self.closed = []
        self.kg = nx.read_gml(self.config['resource_graph'])
        print("🍁 Biplex agent initialized.\n")


    def _solve(self):
        # status, s1 = self.plan_execute(self.goal, domain_file=self.config['bias'])
        # if status:
            # return {'plan':self.env.get_history(), 'final_state':s1, "status":status}

        click.secho(f"Goal: {self.goal}", fg='blue')
        non_exec_domain_file = "agents/biplex/bias/treasure_nonexec.pddl"
        status, s1 = self.plan_execute(goal_in=self.goal, domain_file=non_exec_domain_file, execute=False, fast_mode=False)

        # It's now a resource acquisition problem
        tnode = self._get_goal_object_type(self.goal)
        # s0 = s1
        status, s1 = self.prove(tnode)

        print(f"\nHistory: {self.env.get_history()}")

        return {'plan':[], 'final_state':s1, "status":False}


    def prove(self, tnode):
        # Fast mode planning
        status, s1 = self.plan_execute(f"(have ?x-{str(tnode)})", domain_file=self.config['bias'])
        if status:
            return status, s1

        # Construction
        print("\tExpanding resource graph ...")
        try:
            actions = list(self.kg.predecessors(str(tnode)))
        except:
            print(f"\tType {tnode} does not exist in the resource graph")
            return False, s1
        if not actions:
            print("\tNode exists, but has no predecessor actions")

        while actions:
            anode = actions.pop(0)
            status, s1 = self.ground(anode)
            if status:
                return status, s1

        return False, s1

    def ground(self, anode):
        # Node expansion
        precon_types = list(self.kg.predecessors(str(anode)))
        for tnode in precon_types:
            print(tnode)
            status, s1 = self.prove(tnode=tnode)
            if not status:
                return False, s1

        # once all resources have been acquired, it is time to perform craft action
        # Full fledged navigation and manipulation planning
        print(f"\tAction {anode} is grounded.")
        s0 = s1
        new_domain_file = self._create_new_domain_file(self.kg, anode, self.config['bias'])
        goal = f"(have ?x-{list(self.kg.successors(anode))[0]})"
        status, s1 = self.plan_execute(goal_in=goal, domain_file=new_domain_file, fast_mode=False)
        if status:
            return status, s1
        return False, s1


    def plan_execute(self, goal_in, domain_file, fast_mode=True, execute=True):
        """
        goal = lifted  or grounded
        assume that we only have one predicate
        """
        print(f"\tDomain: {domain_file}")
        s0 = self.env.observe()
        # Update goal by grounding it either with something in the environment or with a hypo
        goal = self._ground_goal(goal_in)
        if not goal:
            return False,s0
        # Create a problem_file
        click.secho(f"Current goal: {goal}", fg='blue')
        goal_line = f"(:goal {goal})"
        init_line = "(:init" + " " + " ".join(set(self.env.observe())) + ")"
        objects = []
        objects_have = []

        state = self.env.observe()
        relevant_objects = set()
        limited_objects = set()
        for literal in state:
            objects_in_lit = literal.replace("(","").replace(")","").split(" ")[1:]
            relevant_objects.update(objects_in_lit)
            if "have" in literal or "inworld" in literal:
                limited_objects.update(objects_in_lit)

        for o in relevant_objects:
            type_val = self.env.objects()[o]
            objects.append(f"{str(o)} - {str(type_val)}")

        for o in limited_objects:
            type_val = self.env.objects()[o]
            objects_have.append(f"{str(o)} - {str(type_val)}")


        # add the object from the goal
        goal_object = goal.replace("(","").replace(")","").split(" ")[1]
        goal_type = goal_in.replace("(","").replace(")","").split(" ")[1].split("-")[1]
        set_objs = set(objects)
        set_objs_have = set(objects_have)


        ################
        if fast_mode:
            goal_entry = f"{goal_object} - {goal_type}"
            if goal_entry not in set_objs:
                # must be constructed since not anywhere in state
                return False, s0
            if goal_entry not in set_objs_have:
                # is available somewhere in the state, but not readily useable
                # might need to focus on acquiring some other resource and return to this
                # return False, s0
                pass
        ####################

        set_objs.add(f"{goal_object} - {goal_type}")
        objects = list(set_objs)

        objects_line = "(:objects" + " " + " ".join(objects) + ")"
        domain_line = "(:domain treasure)" #HACK TODO need to fix
       define_line = "(define (problem treasure)" #HACK TODO fix

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
        problem = _parse(domain_file, self.problem_file)
        task = _ground(problem)
        print("\t*Planning*", end="\r")
        solution = breadth_first_search(task)

        if solution:
            click.secho(f"Plan: {solution}", fg='green')
            if execute:
                print(f"\tExecuting actions:")
                for idx,a in enumerate(solution):
                    click.secho(f"\t\t[{idx}] {a.name}", fg='red')
                    s1 = self.env.step(a.name)
                return True, s1
        print("\tNo plan found")

        return False, s0


    def _create_new_domain_file(self, graph, anode, current_domain):
        action_symbol = f"\t(:action {anode}\n"
        precon_types = list(graph.predecessors(str(anode)))
        precons = []
        effects = []
        params = []
        for p in precon_types:
            variable = "?x"+str(uuid.uuid4())[:3]
            param = f"{variable} - {p}"
            pred = f"(have {variable})"
            effp = f"(not {pred})"
            precons.append(pred)
            effects.append(effp)
            params.append(param)

        eff_types = list(graph.successors(str(anode)))
        for e in eff_types:
            variable = "?y"+str(uuid.uuid4())[:3]
            param = f"{variable} - {e}"
            effp = f"(have {variable})"
            effects.append(effp)
            params.insert(0,param)

        param_line = f"\t\t:parameters ({' '.join(params)})\n"
        precon_line = f"\t\t:precondition (and {' '.join(precons)})\n"
        effects_line = f"\t\t:effect (and {' '.join(effects)}))"

        action_entry = action_symbol+param_line+precon_line+effects_line


        new_domain_filename = current_domain.split(".pddl")[0]+"_gen.pddl"
        with open(current_domain,'r') as current, open(new_domain_filename,'w') as secondfile:
            lines = current.readlines()
            for line in lines[:-1]:
                secondfile.write(line)
            secondfile.write("\n")
            secondfile.write(action_entry)
            secondfile.write("\n")
            secondfile.write(")")

        return new_domain_filename




    def _get_goal_object_type(self, goal):
        name = goal.replace("(","").replace(")","").split(" ")[0]
        args = goal.replace("(","").replace(")","").split(" ")[1:]

        # considering only one arg
        arg = args[0]
        if "?" in arg:
            if "-" in arg:
                typing = arg.split("-")[1]
                return typing
            else:
                raise ValueError("Must provide at least one of constant or a type")
        else:
            raise NotImplementedError("Need to implement a failed planning attempt on a grounded goal")

        return None


    # def _ground_goal(self, atom_str):
        # """
        # Given an atom (have ?x-t) or (have t23) or (on ?x-t y24-y)  or (have ?t34-t)
        # Return (have t23)
        # """
        # objs = self.env.objects()  # CHANGE TO SELF.ENV
        # type_keyed_objs = {}
        # for k,v in objs.items():
            # type_keyed_objs[v.name]= type_keyed_objs.get(v.name,[])
            # type_keyed_objs[v.name].append(k)


        # name = atom_str.replace("(","").replace(")","").split(" ")[0]
        # args = atom_str.replace("(","").replace(")","").split(" ")[1:]
        # new_args = []
        # for arg in args:
            # if "?" in arg:
                # if "-" in arg:
                    # typing = arg.split("-")[1]
                    # if typing in type_keyed_objs:
                        # #Assign random name
                        # new_sym = random.choice(type_keyed_objs[typing])
                        # new_args.append(f"{new_sym}")
                    # else:
                        # #Assign hypothetical name
                        # print("Warning: Gensym-ing a name. Might not work with PDDLGym's constant naming")
                        # hypo_sym = f"{typing}_{str(uuid.uuid4())[:8]}"
                        # new_args.append(f"{hypo_sym}")
                # else:
                    # raise ValueError("Must provide at least one of constant or a type")
            # else:
                # if "-" in arg:
                    # new_arg = arg.split("-")[0]
                    # new_args.append(new_arg)
                # else:
                    # new_args.append(arg)
        # new_atom = "("+name+" "+" ".join(new_args)+")"
        # return new_atom


    def _ground_goal(self, atom_str):
        """
        Given an atom (have ?x-t) or (have t23) or (on ?x-t y24-y)  or (have ?t34-t)
        Return (have t23)
        """
        name = atom_str.replace("(","").replace(")","").split(" ")[0]
        args = atom_str.replace("(","").replace(")","").split(" ")[1:]
        new_args = []
        for arg in args:
            if "?" in arg:
                if "-" in arg:
                    typing = arg.split("-")[1]
                    new_sym, exists = self._find(typing)
                    if exists:
                        new_args.append(f"{new_sym}")
                    else:
                        return None
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




    def _find(self, object_type):
        """
        CONFLATION WARNING: This method accesses self.env.objects( )
        Given an object type, returns an object identifier of that type in the world.
        Returns symbol, True if found. Returns hyposymbol, False if none

        This is meant to simulate the agent's vision system.
        We could imagine searching for it differently
        """
        print(f"\tLooking for object of type {object_type} in the world...")
        # Organize all the objects in the world as a dict  keyed by types
        objs = self.env.objects()  # CHANGE TO SELF.ENV
        type_keyed_objs = {}
        for k,v in objs.items():
            type_keyed_objs[v.name]= type_keyed_objs.get(v.name,[])
            type_keyed_objs[v.name].append(k)

        if object_type in type_keyed_objs:
            new_sym = random.choice(type_keyed_objs[object_type])
            print(f"\tObject {new_sym} of type {object_type} found")
            return new_sym, True

        hypo_sym = f"{object_type}_{str(uuid.uuid4())[:8]}"
        print(f"\tCould not find object of type {object_type}. Gensym: {hypo_sym}")
        return hypo_sym, False





    def _parse_trees_file(self, trees_file):
        trees = []
        # TODO: load file, generate a list of networkx trees
        return trees

