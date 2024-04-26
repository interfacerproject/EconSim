import numpy as np

from .makeragent import MakerAgent
from .resources import Resources
from .work import Work
from .globals import MAX_SUS

class Producer(MakerAgent):
    """Create a product from open designs in the FabLabs ecosystem"""

    def __init__(self, unique_id, model, initial_wealth, living_cost):
        # Pass the parameters to the parent class.
        super().__init__(unique_id, model, initial_wealth, living_cost)

    def work(self):
        self.worked_hours = 0
        # use design to produce
        if Work.get_len_realized_designs() > 0:
            if not Resources.resourses_available() and self.sustainability_level < MAX_SUS:
                # We are not sustainable and we cannot produce, so do nothing
                return
            else:
                if self.start_production():
                    self.is_busy = True
                else:
                    self.is_busy = False
                
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
        if Resources.resourses_available():
            # We can produce unsustainable designs
            idx = np.random.choice(Work.realized_designs)
            Work.start_production(self, idx)
            return True
        else:
            # we need to find a sustainable design
            found = False
            for idx in Work.realized_designs:
                work = Work.work_repository[f'{idx}']
                if Resources.calculate_depletion(work.get_sustainability(hours=False), self.sustainability_level) > 0:
                    # we cannot produce due to lack of resources
                    continue
                else:
                    found = True
                    break
            if found:
                Work.start_production(self, idx)
                return True
        return False

        
    
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
