from agents.agent import Agent
import pddlgym
import networkx as nx
from construct.wrappers import PyperWrapper
from pyperplan.pddl.pddl import Type, Problem, Predicate
from pyperplan.pddl.parser import Parser
from pyperplan.planner import _ground, _search
from pyperplan.grounding import ground
from pyperplan.search.breadth_first_search import breadth_first_search
import random
import uuid
import copy

# state represent: follow pyperplan representation: list of grounded predicates

class BiplexAgent(Agent):
    """
    Biplex
    """

    def __init__(self, ctx):
        super().__init__()
        self.config = ctx
        self.env = PyperWrapper(pddlgym.make(self.config['env']))
        self.env.reset()
        self.root_object_type = Type("object",None)
        self.goal = self._parse_predicate(self.config['goal']) #list of pyper Preds
        self.domain = self._parse_domain(self.config['bias'])  #pyper domain object
        self.trees = self._parse_trees_file(self.config['trees'])
        print("🍁 Biplex agent initialized.")


    def _parse_trees_file(self, trees_file):
        trees = []
        # TODO: load file, generate a list of networkx trees
        return trees

    def _parse_domain(self, dom_file):
        parser = Parser(dom_file) #pyperplan parser
        domain = parser.parse_domain()
        return domain

    def _parse_predicate(self, pred_str):
        """
        Assume a predicate string
        "(have ?x-t)" or "(have p1-p)" or "(on a-block b-block)"
        """
        name = pred_str.replace("(","").replace(")","").split(" ")[0]
        args = pred_str.replace("(","").replace(")","").split(" ")[1:]
        signature = []
        grounded = True
        for arg in args:
            if "-" in arg:
                sym = arg.split("-")[0]
                if "?" in sym:
                    grounded = False
                typing = arg.split("-")[1]
                signature.append((sym, [Type(typing,self.root_object_type)]))
            else:
                if "?" in arg:
                    raise ValueError("Must provide at least one of constant or a type")
                objs = self.env.objects()
                typing = objs[arg]
                signature.append((arg, [typing]))
        return Predicate(name, signature)

    def _assign_symbol(self, predicate): # ADD SELF
        """
        Replaces ?x with either a hypothetical or with an object from the domain
        """
        predicate_copy = copy.deepcopy(predicate)
        # Flip objects dictionary to be keyed to type name
        objs = self.env.objects()  # CHANGE TO SELF.ENV
        type_keyed_objs = {}
        for k,v in objs.items():
            type_keyed_objs[v.name]= type_keyed_objs.get(v.name,[])
            type_keyed_objs[v.name].append(k)

        updated_signature = []
        for term,typing in predicate_copy.signature:
            if "?" in term:
                # check if env objects have an object of type
                if typing[0].name in type_keyed_objs:
                    # randomly assign
                    used_term = random.choice(type_keyed_objs[typing[0].name])
                    updated_signature.append((used_term, [typing[0]]))
                else:
                    # hypothetical name
                    hypo_term = typing[0].name+"_"+str(uuid.uuid4())[:8]
                    updated_signature.append((hypo_term, [typing[0]]))
            else:
                 updated_signature.append((term, [typing]))
        predicate_copy.signature = updated_signature
        return predicate_copy


    def _solve(self):
        status, s1 = self.prove()
        if status:
            return {'plan':[], 'final_state':s1, "status":status}
        return {'plan':[], 'final_state':s1, "status":False}


    def plan_execute(self):
        """
        goal = lifted  or grounded
        assume that we only have one predicate
        """
        goal_updated = self._assign_symbol(self.goal)
        print(self.domain)
        print(self.env.objects())
        problem = Problem("treasure", self.domain, self.env.objects(), self.env.observe(), [goal_updated])
        print(problem)
        task = _ground(problem)
        print(task)
        plan = breadth_first_search(task)
        print(plan)

        return False, []

    def prove(self):
        status, s1 = self.plan_execute()
        print(status, s1)
        return False, []


