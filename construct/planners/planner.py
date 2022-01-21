from abc import abstractmethod, ABC

class Planner(ABC):
    """
    Abstract PLanner class
    """

    @abstractmethod
    def _plan(self, domain_file, problem_file):
        pass

    def plan(self, domain_file, problem_file):
        return self._plan(domain_file, problem_file)

