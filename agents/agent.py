from abc import abstractmethod, ABC

class Agent(ABC):
    """
    Main Agent claims
    """

    @abstractmethod
    def _solve(self):
        pass

    def solve(self):
        return self._solve()
