import numpy as np
from .makeragent import MakerAgent
from .work import Work

class Designer(MakerAgent):
    """A Designer in the FabLabs ecosystem"""

    def __init__(self, unique_id, model, initial_wealth, living_cost):
        # Pass the parameters to the parent class.
        super().__init__(unique_id, model, initial_wealth, living_cost)

    def work(self):
        self.is_busy = True
        self.worked_hours = 0
        if self.create_or_adapt() == "create":
            # create design, choice is not important (they are all the same)
            Work.start_design(self)
        else:
            # adapt design
            self.adapt_design()

    def work_is_done(self):
        # INTELLIGENCE REQUIRED!
        # Criteria to determine whether the maker has worked enough
        # if np.random.binomial(1, 0.5) > 0:
        #     return True
        # return False
        return True

    def finish_work(self):
        Work.add_contribution(self)
        Work.set_design_ready(self)
        self.worked_hours = 0
        self.is_busy = False

    def adapt_design(self):
        # INTELLIGENCE REQUIRED!
        # Some strategy on what design to pick?
        # Now random
        design_id = np.random.choice(Work.realized_designs)
        Work.improve_design(self, design_id)

    def create_or_adapt(self):
        # INTELLIGENCE REQUIRED!
        if Work.get_len_realized_designs() > 0 :
            if np.random.binomial(1, 0.5) > 0 :
                return "adapt"
        return "create"
