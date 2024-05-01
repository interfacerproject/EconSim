import numpy as np

from .work import Work
from .utils import norml
from .globals import get_debug

class Market():
    
    # we collect this information to tune the threshold
    max_score = 0
    
    @classmethod
    def get_max_score(cls):
        return cls.max_score
    
    def __init__(self, weights, threshold, competition):
        

        price_weight, quality_weight, sustainability_weight = weights

        if price_weight > 0 or abs(price_weight) > 1:
            raise Exception(f"Price weight needs to be non positive and less than 1 in abs value, iso {price_weight}")
        elif quality_weight < 0 or abs(quality_weight) > 1:
            raise Exception(f"Quality weight needs to be non negative and less than 1 in abs value, iso {quality_weight}")
        elif sustainability_weight < 0 or abs(sustainability_weight) > 1:
            raise Exception(f"Sustainability weight needs to be non negative and less than 1 in abs value, iso {sustainability_weight}")
        elif abs(price_weight) +  abs(quality_weight) + abs(sustainability_weight) > 1:
            raise Exception(f"Sum of abs weight values needs to be less than 1, iso {abs(price_weight) +  abs(quality_weight) + abs(sustainability_weight)}")
        
        self.weights = [price_weight, quality_weight, sustainability_weight]
        self.threshold = threshold
        self.competition = competition


    def step(self):
        # buy from open design
        # product_id = random.choice(Work.on_sale_products)
        if not Work.get_len_on_sale_products() >= self.competition:
            return
        
        ids = []
        price_arr = []
        quality_arr = []
        sustainability_arr = []
        for product_id in Work.on_sale_products:
            work_to_buy = Work.work_repository[f'{product_id}']
            ids.append(product_id)
            price_arr.append(work_to_buy.get_price())
            quality_arr.append(work_to_buy.get_quality())
            sustainability_arr.append(work_to_buy.get_sustainability())

        id_to_buy, Market.max_score = self.pick_product(ids, price_arr, quality_arr, sustainability_arr)
        if id_to_buy != None:
            work_to_buy = Work.work_repository[f'{id_to_buy}']
            work_to_buy.redistribute_profit()
            Work.buy(id_to_buy)
            

    def pick_product(self, ids, price_arr, quality_arr, sustainability_arr):
        # INTELLIGENCE REQUIRED!
        # Some strategy on what design to pick?
        max_score = -10000
        min_score = 10000
        chosen_id = None
        # set_trace()
        # price_arr = norml(price_arr)
        # quality_arr = norml(quality_arr)
        # sustainability_arr = norml(sustainability_arr)
        for i,prod_id in enumerate(ids):
            # score = np.sum(np.array([price_arr[i], quality_arr[i], hours_arr[i]]) * np.array(self.weights))
            # breakpoint()
            score = np.sum(np.array([price_arr[i], quality_arr[i], sustainability_arr[i]]) * np.array([self.weights]))
            if score > max_score:
                max_score = score
                chosen_id = prod_id
            if score < min_score:
                min_score = score
            # if get_debug() and score < -100:
            #     breakpoint()

        
        if get_debug() and min_score < self.threshold:
            print(f"Threshold: {self.threshold} effective with min score: {min_score}")

        if max_score > self.threshold:
            if get_debug():
                print(f"lenghth items: {len(ids)}, max score: {max_score}, threshold: {self.threshold}, weights: {self.weights}")
                i = ids.index(chosen_id)
                print(f"price: {price_arr[i]}, quality: {quality_arr[i]}, sustainability: {sustainability_arr[i]}")
                # breakpoint()
            return chosen_id, max_score
        else:
            if get_debug():
                print(f"Threshold: {self.threshold} effective with max score: {max_score}")
        return None, max_score
    
    def get_price_weight(self):
        return self.weights[0]
    
    def get_quality_weight(self):
        return self.weights[1]
    
    def get_sustainability_weight(self):
        return self.weights[2]