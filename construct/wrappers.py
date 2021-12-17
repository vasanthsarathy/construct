import gym
from pddlgym.structs import Predicate, Literal, TypedEntity, Type

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

            obj_type = Type(obj_type_str)
            obj_const = obj_type(obj_const_str)
            objs.append(obj_const)
        actionP = Predicate(name, len(args))
        action = Literal(actionP, objs)
        return action


