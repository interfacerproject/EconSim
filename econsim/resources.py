
from .globals import get_debug, EPS, MAX_SUS, MIN_SUS

class Resources():
    initial_amount = 0
    current_amount = 0

    @classmethod
    def init(cls, initial_amount):
        # breakpoint()
        cls.initial_amount = initial_amount
        cls.current_amount = cls.initial_amount

    @classmethod
    def get_amount_resources(cls):
        return cls.current_amount
    

    @classmethod
    def calculate_depletion(cls, work, producer):
        # breakpoint()
        if producer.worked_hours == 0:
            #  producer is evaluating whether the design can be produced
            sus_level = (work.get_sustainability()/work.get_hours() + (MAX_SUS + MIN_SUS)/2 + producer.sustainability_level)/2
        else:
            #  producer is already one of the contributors
            sus_level = work.get_sustainability()/work.get_hours() + (MAX_SUS + MIN_SUS)/2
        comsumption = (MAX_SUS - sus_level) 
        if cls.current_amount <= 0:
             det = EPS 
        else:
             det = cls.current_amount
        cost = comsumption / (det/cls.initial_amount)
        cls.current_amount = max(cls.current_amount - comsumption,0)
        if get_debug():
                print(f"Cost depletion: {cost}")
        if cost < 0:
             raise Exception(f"Material cost is negative, should not happen")
        return cost


    @classmethod
    def resourses_available(cls):
        if cls.current_amount <= 0:
            # breakpoint()
            if get_debug():
                print("Resources depleted")
            return False
        return True

        

