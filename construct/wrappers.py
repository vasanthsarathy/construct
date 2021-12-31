import gym
import pddlgym.structs as pgym
import pyperplan.pddl.pddl as pyper


"""
Bunch of wrappers useful to convert between PDDLGym and other representations
"""

# String Wrapper
class StringWrapper(gym.Wrapper):
    """
    Allows for providing actions as strings rather than the pddlgym representation
    """
    def __init__(self, env):
        super().__init__(env)
        self.env = env

    def step(self,action_str):
        action = self._str_to_action(action_str)
        print(f"Action: {action}", type(action))
        next_state, reward, done, info = self.env.step(action)
        return next_state, reward, done, info

    def _str_to_action(self, action_str):
        name = action_str.split("(")[0]
        args = action_str.split("(")[1].split(")")[0].split(",")
        objs = []
        for arg in args:
            arg = arg.replace(" ","")
            obj_type_str = arg.split(":")[1]
            obj_const_str = arg.split(":")[0]

            obj_type = pgym.Type(obj_type_str)
            obj_const = obj_type(obj_const_str)
            objs.append(obj_const)
        actionP = pgym.Predicate(name, len(args))
        action = pgym.Literal(actionP, objs)
        return action

# pyperplan wrapper
class PyperWrapper(gym.Wrapper):
    """
    Allows for translating between pddlgym and pyperplan representations.
    Can run pyperplan solutions in pddlgym
    Can read pddlgym output in pyperplan state representation
    """
    def __init__(self, env):
        super().__init__(env)
        self.env = env
        self.current_state = None  # going to be in default pddlgym representation
        self.root_object_type = pyper.Type("object",None)
        self.history = [] #In pyperplan format

    def reset(self, **kwargs):
        obs = self.env.reset(**kwargs)
        self.current_state = obs
        return self.observe()

    def observe(self, source='pypertask'):
        if source == 'pyperpred':
            return self._obs_pddlgym_to_pyper(self.current_state)
        if source == 'pddlgym':
            return self.current_state
        if source == 'pypertask':
            return self._obs_pddlgym_to_pypertask(self.current_state)
        raise ValueError("source must be either 'pyper' or 'pddlgym'")

    def objects(self):
        """
        Returns all the objects in the current state
        """
        objects = {}
        objs = self.current_state[0].objects
        for o in set(objs):
            key = o.name
            type_name = str(o.var_type)
            value = pyper.Type(type_name, self.root_object_type)
            objects.update({key : value})
        return objects



    def step(self,action):
        action_pddlgym = self._action_pyper_to_pddlgym(action)
        next_state = self.env.step(action_pddlgym)
        self.history.append(action)
        self.current_state = next_state

        return self.observe()

    def get_history(self):
        return self.history

    def _action_pyper_to_pddlgym(self, action):
        """
        (move p3 k1) --> pddlgym representation
        """
        name = action.replace("(","").replace(")","").split(" ")[0]
        objs = set(self.current_state[0].objects)
        args = action.replace("(","").replace(")","").split(" ")[1:]
        arity = len(args)
        typed_args = [ (lambda x: [x for x in objs if x == y][0])(y) for y in args]
        action_pddlgym = pgym.Literal(pgym.Predicate(name, arity), typed_args)
        return action_pddlgym


    def _obs_pddlgym_to_pyper(self, obs):
        predicates = []
        for item in set(obs[0].literals):
            name = str(item).split("(")[0]
            list_args_str = str(item).split("(")[1].split(")")[0].split(",")
            signature = [(x.split(":")[0], [pyper.Type(x.split(":")[1], self.root_object_type)]) for x in list_args_str]
            pred = pyper.Predicate(name, signature)
            predicates.append(pred)
        return predicates

    def _obs_pddlgym_to_pypertask(self, obs):
        literals = []
        for item in set(obs[0].literals):
            name = str(item).split("(")[0]
            list_args_str = str(item).split("(")[1].split(")")[0].split(",")
            new_args = [x.split(":")[0] for x in list_args_str]
            new_lit = "("+name+" "+" ".join(new_args)+")"
            literals.append(new_lit)
        return frozenset(literals)

