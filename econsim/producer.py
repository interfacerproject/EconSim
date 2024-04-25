import numpy as np

from .makeragent import MakerAgent
from .resources import Resources
from .work import Work

class Producer(MakerAgent):
    """Create a product from open designs in the FabLabs ecosystem"""

    def __init__(self, unique_id, model, initial_wealth, living_cost):
        # Pass the parameters to the parent class.
        super().__init__(unique_id, model, initial_wealth, living_cost)

    def work(self):
        # use design to produce
        if Work.get_len_realized_designs() > 0 and Resources.resourses_available():
            self.is_busy = True
            self.worked_hours = 0
            self.start_production()

    def work_is_done(self):
        # INTELLIGENCE REQUIRED!
        # Criteria to determine whether the maker has worked enough
        # if np.random.binomial(1, 0.5) > 0 :
        #     return True
        # return False
        return True

    def finish_work(self):
        Work.add_contribution(self)
        Work.set_product_ready(self)
        self.worked_hours = 0
        self.is_busy = False

    def start_production(self):
        # INTELLIGENCE REQUIRED!
        # Some strategy on what design to pick?
        # Now random
        idx = np.random.choice(Work.realized_designs)
        Work.start_production(self, idx)
    
    # def choose_design(self):
    #     # Possible strategy
    #     max_hours = 0
    #     idx = -1
    #     for i in Work.realized_designs:
    #         a_work = Work.work_repository[f'{i}']
    #         if a_work.get_hours() > max_hours:
    #             max_hours = a_work.get_hours()
    #             idx = i
    #     return(idx)        
