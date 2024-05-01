import numpy as np
from .resources import Resources
from .utils import agent_type
from .globals import MAX_FEE, MIN_FEE, MAX_SUS, MIN_SUS, MAX_QUALITY, MIN_QUALITY

class Work():
    # list of designs being worked on (being designed)
    designs_in_progress = []
    # list of designs that have been designed and could be either produced or improved (by a designer)
    realized_designs = []
    
    # list of designs that are being realised as products
    products_in_progress = []
    # list of products that have been produced
    on_sale_products = []

    # list of products that have been sold
    sold_products = []

    # containers of works
    design_titles = []
    design_images = []
    current_design_id = 0
    work_repository = {}

    model = None

    tot_contributors = 0
    tot_hours = 0
    tot_prices = 0
    tot_quality_level = 0
    tot_sustainability_level = 0
    tot_material_cost = 0


    @classmethod
    def init_thingiverse(cls):
        # The following represents a list of real object extracted from Thingiverse
        TITLES = ["Openscad_Wrench","Braille_Generator","Power_strip_mount_parameterized","Adapter_from_a_saw_to_a_vac_cleaner","Parametric_Cable_Clip","Small_150A_busbar","Charging_stand_-_MagSafe_and_Pixel_Watch_2","fence_connector_","Filament_spool_cable_reel","Parametric_Under_Shelf_Storage","Customizable_Hole_Gauge","Slashlight_Stand_2.0","Customizable_Box_with_Magnetic_Lid","Headphone_desk_holder","Outil_a_deviser_les_pointes_de_fleches-lames","Pince_a_aiguiser_les_Exodus_QAD_","BASIC_GRADED_CARD_STAND","CNC_Workholding_Clamp_Customizable","Parametric_Shelf_Book_Divider","Solar_filter_-_front_ring","Braille_Generator","Power_strip_mount_parameterized","Adapter_from_a_saw_to_a_vac_cleaner","Parametric_Cable_Clip","Small_150A_busbar","Charging_stand_-_MagSafe_and_Pixel_Watch_2","fence_connector_","Filament_spool_cable_reel","Parametric_Under_Shelf_Storage","Customizable_Hole_Gauge","Slashlight_Stand_2.0","Customizable_Box_with_Magnetic_Lid","Headphone_desk_holder","Outil_a_deviser_les_pointes_de_fleches-lames","Pince_a_aiguiser_les_Exodus_QAD_","CNC_Workholding_Clamp_Customizable","BASIC_GRADED_CARD_STAND","Sky_Puck_Wall_Mount","Parametric_Shelf_Book_Divider","Solar_filter","Clamp_hook","Solar_filter","Polyamory_Spice_Rack","Text_art_2_directions","clamp_screwdriver","Safe-T-Sparkler_Holder","V8_aaa_battery_holder","Miniature_Rectangular_Angled_Base_Adaptor","Customizable_soap_press_sleeve","Bases_and_Trays","clamp_screwdriver","Parametric_Dice_Tray,_Tablet_Holder,_and_Storage_Box","phone_stand_R9","Customizable_Magura_MT5/MT7_Brake_Caliper_Cover_Rings","EV_charge_plug_holder","spring_plate_2","____Thing_to_connect_aluminum_profiles_invisible","No_support_Hinge_Mortise_w_center_line","Violin_microphone_clamp","Anti_wobble_monitor_stand","Parametric_Shelf_Bookend","Parametric_Corner_case_for_controls","DigiRoller_-_A_digital_die_roller","Magnifying_Glass_Frame_-_parametric","Fellowes_Monitor_Stand_Legs","Sonoff_Zigbee_Wall_Mount","Vertical_Breathe_Right_Strip_Box","Upside_Down_Bottle_Holder","Basket_Container_Labels","bearing_spacer","spring_plate_5","More_robust_joint_for_Leifheit_Classic_Tower_340","Weather_Station_v2_-_Pluviometer_v2","Telescope_solar_filter","Parkside_PKHAP_20-Li_B2_Hammer_Drill_vacuum_adapter","Heart_Vase","Peace_necklace_(customizable)","Königinnen_Absperrgitter","Test_HB","Square_drive_holder","Rotary_Handle_with_Aqara_ZigBee_Sensor","Square_drive_holder","spring_plate_3","spring_plate_4","Emmett's_Three_Cube_Gears_1-2_Scale,_But_Parts_Are_Separated","wemos_stack_ver2","Filament_Spool_Spindle","Doxy_Replacement_Shell","i3_PTFE_tube_cutting_measure","bot","LinuxCNC_homing_visualization","Bullet_Mixer_Adapter__Ring","Single_shot_magazine_Snowpeak_with_Openscad"]
        IMGS = ["https://cdn.thingiverse.com/assets/46/86/44/6b/5d/card_preview_8d31553e-846c-45da-b3b5-81b990a9a394.png","https://cdn.thingiverse.com/assets/39/3b/32/62/8d/card_preview_4721e15b-0ddb-484f-aef7-95a1f841bb11.png","https://cdn.thingiverse.com/assets/60/eb/64/2c/fd/card_preview_078d2099-a43d-46bb-a413-f2026aed32d8.png","https://cdn.thingiverse.com/assets/cd/7e/f5/16/cf/card_preview_035724cc-8e20-447b-a7d3-48b98d8ed793.jpeg","https://cdn.thingiverse.com/assets/db/0b/5c/c2/9f/card_preview_74e74ea0-aee5-4ddf-b313-bd4e7396254b.jpg","https://cdn.thingiverse.com/assets/1f/fb/34/91/63/card_preview_626153e8-f573-4653-a322-300fb849dbda.png","https://cdn.thingiverse.com/assets/3a/87/ef/a7/3c/card_preview_c768e55c-813c-4bd9-aa2b-91dad0d6f96f.jpg","https://cdn.thingiverse.com/assets/18/23/5d/7f/8a/card_preview_1e3b0bae-56b0-47a7-81bf-3e1d27016e98.JPG","https://cdn.thingiverse.com/assets/f9/e7/88/50/b3/card_preview_af8d1f06-31e0-41cf-829a-a9d2e615280e.jpg","https://cdn.thingiverse.com/site/img/default/Gears_preview_card.jpg","https://cdn.thingiverse.com/assets/92/47/cf/48/25/card_preview_b64c0a9b-ef60-460e-8a53-a9f2d6d9502c.jpg","https://cdn.thingiverse.com/assets/fc/19/57/20/a9/card_preview_e523b72b-ad83-4cc6-a5d9-676d9934cf5b.png","https://cdn.thingiverse.com/assets/80/9a/c1/94/6f/card_preview_magnetic_box.png","https://cdn.thingiverse.com/assets/15/05/6a/65/6a/card_preview_2eda5cec-1fdd-4e7b-9c8f-f5541a62e468.png","https://cdn.thingiverse.com/assets/3d/ee/92/70/65/card_preview_5dc2c6a6-1256-4c4d-8fa4-9fa2fe8e6cd8.png","https://cdn.thingiverse.com/assets/27/6f/b6/5c/f0/card_preview_8faa1e75-d5e7-4884-a15d-82aab114895c.png","https://cdn.thingiverse.com/assets/29/f8/21/81/36/card_preview_9efdd59f-448b-4199-adcd-cd82406d9a3d.png","https://cdn.thingiverse.com/assets/af/4e/b7/ce/87/card_preview_c9ce3ba9-f637-4e86-8c2a-e2b8ca36f67e.png","https://cdn.thingiverse.com/assets/d0/32/3e/cc/83/card_preview_4066d243-0c14-480c-a783-9d7b9397677a.png","https://cdn.thingiverse.com/assets/ef/50/64/19/17/card_preview_2adfc220-58fc-480e-a982-df3a65f8d49e.png","https://cdn.thingiverse.com/assets/39/3b/32/62/8d/card_preview_4721e15b-0ddb-484f-aef7-95a1f841bb11.png","https://cdn.thingiverse.com/assets/60/eb/64/2c/fd/card_preview_078d2099-a43d-46bb-a413-f2026aed32d8.png","https://cdn.thingiverse.com/assets/cd/7e/f5/16/cf/card_preview_035724cc-8e20-447b-a7d3-48b98d8ed793.jpeg","https://cdn.thingiverse.com/assets/db/0b/5c/c2/9f/card_preview_74e74ea0-aee5-4ddf-b313-bd4e7396254b.jpg","https://cdn.thingiverse.com/assets/1f/fb/34/91/63/card_preview_626153e8-f573-4653-a322-300fb849dbda.png","https://cdn.thingiverse.com/assets/3a/87/ef/a7/3c/card_preview_c768e55c-813c-4bd9-aa2b-91dad0d6f96f.jpg","https://cdn.thingiverse.com/assets/18/23/5d/7f/8a/card_preview_1e3b0bae-56b0-47a7-81bf-3e1d27016e98.JPG","https://cdn.thingiverse.com/assets/f9/e7/88/50/b3/card_preview_af8d1f06-31e0-41cf-829a-a9d2e615280e.jpg","https://cdn.thingiverse.com/site/img/default/Gears_preview_card.jpg","https://cdn.thingiverse.com/assets/92/47/cf/48/25/card_preview_b64c0a9b-ef60-460e-8a53-a9f2d6d9502c.jpg","https://cdn.thingiverse.com/assets/fc/19/57/20/a9/card_preview_e523b72b-ad83-4cc6-a5d9-676d9934cf5b.png","https://cdn.thingiverse.com/assets/80/9a/c1/94/6f/card_preview_magnetic_box.png","https://cdn.thingiverse.com/assets/15/05/6a/65/6a/card_preview_2eda5cec-1fdd-4e7b-9c8f-f5541a62e468.png","https://cdn.thingiverse.com/assets/3d/ee/92/70/65/card_preview_5dc2c6a6-1256-4c4d-8fa4-9fa2fe8e6cd8.png","https://cdn.thingiverse.com/assets/27/6f/b6/5c/f0/card_preview_8faa1e75-d5e7-4884-a15d-82aab114895c.png","https://cdn.thingiverse.com/assets/af/4e/b7/ce/87/card_preview_c9ce3ba9-f637-4e86-8c2a-e2b8ca36f67e.png","https://cdn.thingiverse.com/assets/29/f8/21/81/36/card_preview_9efdd59f-448b-4199-adcd-cd82406d9a3d.png","https://cdn.thingiverse.com/assets/7a/62/09/d0/d0/card_preview_f6488322-22f4-4483-98bf-edfe5643d3ff.jpg","https://cdn.thingiverse.com/assets/d0/32/3e/cc/83/card_preview_4066d243-0c14-480c-a783-9d7b9397677a.png","https://cdn.thingiverse.com/assets/81/fc/cd/08/5e/card_preview_84dfe360-fffd-426d-9333-973f651b54c7.jpeg","https://cdn.thingiverse.com/assets/f8/65/98/54/1c/card_preview_bede6d54-d836-4ec5-a1f7-2a8b5ddd9e38.png","https://cdn.thingiverse.com/assets/81/fc/cd/08/5e/card_preview_84dfe360-fffd-426d-9333-973f651b54c7.jpeg","https://cdn.thingiverse.com/assets/6b/6a/c1/ed/52/card_preview_c6bb9354-3e99-4c73-851f-3436a01251a9.png","https://cdn.thingiverse.com/assets/5d/4b/11/92/46/card_preview_2ae5262b-d2e4-417f-a7d4-1b56a2cb2b6c.png","https://cdn.thingiverse.com/assets/d9/20/b4/a5/09/card_preview_aafd3b8b-c412-4fa9-a942-d2d13f34dd59.png","https://cdn.thingiverse.com/assets/52/99/a1/12/21/card_preview_0b2bc0c1-6938-42ed-8633-7cfaf5f772a7.jpg","https://cdn.thingiverse.com/assets/88/e3/cc/c2/70/card_preview_9f7c2fec-8e17-423a-80cf-63dfb2c91e5f.png","https://cdn.thingiverse.com/assets/f9/0f/26/41/f3/card_preview_8f007137-7ba1-4bd1-a63b-dff4dc502d94.jpg","https://cdn.thingiverse.com/assets/d3/31/ec/d8/73/card_preview_f4bdc47a-27b6-4d4e-ab2c-4fb15fa2be91.jpg","https://cdn.thingiverse.com/assets/a0/3a/fa/40/43/card_preview_4688cddc-b1d4-4fa0-bc59-03233fb5a353.png","https://cdn.thingiverse.com/assets/0c/2b/0c/fb/3d/card_preview_clampscrdrwr.jpg","https://cdn.thingiverse.com/assets/34/89/a8/71/39/card_preview_13d6b739-5fe2-494e-b078-b6f82e6541b1.jpg","https://cdn.thingiverse.com/assets/6c/b0/fa/a0/9e/card_preview_44f8bb90-5765-4dc8-a0f6-50298831c086.jpg","https://cdn.thingiverse.com/assets/17/9b/f5/70/ec/card_preview_aec025a2-577b-414b-a700-473bfc9114c3.jpg","https://cdn.thingiverse.com/assets/b9/86/e3/3b/13/card_preview_b288cd38-fa0e-48ff-aa42-bd1ae8441e8a.jpg","https://cdn.thingiverse.com/assets/ed/fd/cf/79/ba/card_preview_2422a384-4468-4bed-ac5b-70a1a28d4c31.png","https://cdn.thingiverse.com/assets/69/60/06/d1/12/card_preview_be210998-3c55-45f2-b993-c499b27fd19e.png","https://cdn.thingiverse.com/assets/c6/85/c4/2c/d2/card_preview_6755f692-6b70-4ff2-b60f-4386281f01e6.png","https://cdn.thingiverse.com/assets/58/50/23/d3/b3/card_preview_cb6a0e41-a437-4476-a9d6-34bb34afedcf.jpg","https://cdn.thingiverse.com/assets/7a/f1/89/5b/ce/card_preview_8d987903-da8c-4a7e-a485-3af0d3d4b11c.png","https://cdn.thingiverse.com/assets/6a/57/9d/61/67/card_preview_60ff5182-2193-4e44-be25-e18dc8f5523f.png","https://cdn.thingiverse.com/assets/78/79/14/cd/d8/card_preview_eb5869b1-36b3-42dc-a5b8-61541fe92ab1.png","https://cdn.thingiverse.com/assets/26/1a/b4/54/b8/card_preview_7f794299-1caa-410c-8b04-4443df76f670.jpg","https://cdn.thingiverse.com/assets/f3/44/00/a9/5b/card_preview_345f46f6-734a-4df8-931a-9c04652e5fd3.jpg","https://cdn.thingiverse.com/assets/34/95/ac/99/07/card_preview_55e9d585-f69e-4de6-ab83-57aaceacc177.png","https://cdn.thingiverse.com/assets/a5/51/c3/64/73/card_preview_473c34c1-2443-4d42-80f2-d22ab76307ec.png","https://cdn.thingiverse.com/assets/36/ec/f9/83/75/a8d6e32b-db54-4892-8ee9-56550ed220ce.webp","https://cdn.thingiverse.com/assets/8f/78/3e/a2/c4/card_preview_2debf8ff-a98f-4277-a77e-3ac28d29db27.png","https://cdn.thingiverse.com/assets/a2/f9/67/9a/5e/card_preview_dd633df4-8e1a-4bc1-93d1-9d7461cb2f38.jpg","https://cdn.thingiverse.com/site/img/default/Gears_preview_card.jpg","https://cdn.thingiverse.com/assets/a6/a5/a3/14/ce/card_preview_0de78a6d-2920-4474-879a-ab3c49f36bd3.jpg","https://cdn.thingiverse.com/site/img/default/Gears_preview_card.jpg","https://cdn.thingiverse.com/site/img/default/Gears_preview_card.jpg","https://cdn.thingiverse.com/site/img/default/Gears_preview_card.jpg","https://cdn.thingiverse.com/assets/50/f4/64/32/51/card_preview_694c039e-6d13-49b7-a5a2-1a116c1dda01.jpg","https://cdn.thingiverse.com/assets/7b/ac/7d/5e/0b/card_preview_b7f7d853-5e87-4ded-9bbd-6f647b95bb20.png","https://cdn.thingiverse.com/assets/fc/9c/73/4d/d9/card_preview_b2d8dd4c-4fb7-4657-b0ff-fdfc38885348.png","https://cdn.thingiverse.com/assets/e6/26/47/f5/a7/card_preview_365359ba-c90f-4de2-8ee5-76b3a74387de.png","https://cdn.thingiverse.com/site/img/default/Gears_preview_card.jpg","https://cdn.thingiverse.com/assets/61/bb/f4/75/83/card_preview_c81841ee-f5c7-456e-8f15-2fe508050c4c.png","https://cdn.thingiverse.com/assets/d7/bf/b0/fa/2b/card_preview_4f2c668a-cfe3-47db-a6d6-fd917627af59.png","https://cdn.thingiverse.com/assets/61/bb/f4/75/83/card_preview_c81841ee-f5c7-456e-8f15-2fe508050c4c.png","https://cdn.thingiverse.com/assets/63/67/d2/e1/8e/card_preview_2ed5ad2a-e22b-4537-a7d3-7d9295dd8778.jpg","https://cdn.thingiverse.com/assets/26/56/70/7d/81/card_preview_7411d3a8-fb94-48c5-b652-fa613cc2a3a0.png","https://cdn.thingiverse.com/assets/2b/6e/72/f1/3a/card_preview_571c8dfb-493b-4e4c-88c7-fe4b25173542.png","https://cdn.thingiverse.com/assets/00/20/be/a1/12/card_preview_59d45d09-17cf-484f-b2b9-7ea58ed8b044.png","https://cdn.thingiverse.com/assets/69/e6/fe/bd/83/card_preview_5880da4f-04d8-4d5b-9b8e-19a131da3686.png","https://cdn.thingiverse.com/assets/92/fd/7e/85/73/card_preview_631978b6-b3fb-4c07-b8e3-e16528d6f27a.png","https://cdn.thingiverse.com/assets/1f/2d/f3/0b/8e/card_preview_513684df-07bb-42ca-a6a8-3310bc67ffe2.png","https://cdn.thingiverse.com/assets/ab/0f/82/a8/ad/card_preview_7976af6e-593f-4af6-8fcf-9aa4a3b3d55d.jpg","https://cdn.thingiverse.com/assets/5a/78/87/7d/e7/card_preview_753e32f2-e309-4fde-bf5d-5f29c7c4eab7.png","https://cdn.thingiverse.com/assets/df/de/a3/0e/31/card_preview_bb7efab1-fce7-41e4-be63-39814a936a13.png","https://cdn.thingiverse.com/assets/c8/bd/a2/3e/12/card_preview_12c7c15d-c65b-41cd-9c71-67169cfc5af2.jpg"]

        assert len(TITLES) == len(IMGS)
        cls.design_titles = []
        cls.design_images = []
        for i in range(len(TITLES)):
            if TITLES[i] not in cls.design_titles:
                cls.design_titles.append(TITLES[i])
                cls.design_images.append(IMGS[i])

        assert len(cls.design_titles) == len(cls.design_images)

        # print(f"There are {len(TITLES)} objects in the ecosystem")

        
    @classmethod
    def init_works(cls, model, method):
        cls.init_thingiverse()

        cls.designs_in_progress = []
        cls.realized_designs = []
        cls.products_in_progress = []
        cls.on_sale_products = []
        cls.sold_products = []
        
        cls.current_design_id = np.random.randint(len(cls.design_titles))
        cls.work_repository = {}

        cls.tot_contributors = 0
        cls.tot_hours = 0
        cls.tot_prices = 0
        cls.tot_quality_level = 0
        cls.tot_sustainability_level = 0
        cls.tot_material_cost = 0

        cls.model = model
        if method == 1:
            cls.method = "producers"
        elif method == 2:
            cls.method = "equal"
        elif method == 3:
            cls.method = "proportional"
        else:
            raise Exception(f"Method {method} is not recognised")

    
    @classmethod
    def get_len_designs_in_progress(cls):
        return len(cls.designs_in_progress)

    @classmethod
    def get_len_realized_designs(cls):
        return len(cls.realized_designs)

    @classmethod
    def get_len_products_in_progress(cls):
        return len(cls.products_in_progress)

    @classmethod
    def get_len_on_sale_products(cls):
        return len(cls.on_sale_products)

    @classmethod
    def get_len_sold_products(cls):
        return len(cls.sold_products)

    @classmethod
    def get_avrg_contr_sold_goods(cls):        
        nr_items = max(len(cls.sold_products),1)
        return cls.tot_contributors/nr_items

    @classmethod
    def get_avrg_hours_sold_goods(cls):        
        nr_items = max(len(cls.sold_products),1)
        return cls.tot_hours/nr_items

    @classmethod
    def get_avrg_prices_sold_goods(cls):        
        nr_items = max(len(cls.sold_products),1)
        return cls.tot_prices/nr_items

    @classmethod
    def get_avrg_quality_sold_goods(cls):        
        nr_items = max(len(cls.sold_products),1)
        return cls.tot_quality_level/nr_items

    @classmethod
    def get_avrg_sus_sold_goods(cls):        
        nr_items = max(len(cls.sold_products),1)
        return cls.tot_sustainability_level/nr_items

    @classmethod
    def get_avrg_mat_cost_sold_goods(cls):        
        nr_items = max(len(cls.sold_products),1)
        return cls.tot_material_cost/nr_items

    @classmethod
    def start_design(cls, agent)-> None:
        """
            Start work on a design, since all design are equal
            we start them in round-robin
        """
        working_on_id = cls.current_design_id
        cls.current_design_id = cls.current_design_id + 1
        cls.designs_in_progress.append(working_on_id)
        title_index = working_on_id%len(cls.design_titles)
        new_work = Work(working_on_id, cls.design_titles[title_index], cls.design_images[title_index])
        cls.work_repository[f'{working_on_id}'] = new_work

        agent.working_on_id = working_on_id

    @classmethod
    def start_production(cls, agent, design_id)-> None:

        if design_id not in cls.realized_designs:
            raise Exception(f"{design_id} is not in realized_designs")

        # TODO: here starting production means that
        # the design is taken out of the designs
        # that can be improved.
        cls.realized_designs.remove(design_id)
        cls.products_in_progress.append(design_id)                
            
        agent.working_on_id = design_id

    @classmethod
    def set_design_ready(cls, agent):
        # set_trace()
        work = cls.work_repository[f'{agent.working_on_id}']
        cls.designs_in_progress.remove(agent.working_on_id)
        cls.realized_designs.append(agent.working_on_id)
        work.set_status("designed")
        
        # reset the id of the agent
        agent.working_on_id = None

    @classmethod
    def set_product_ready(cls, agent):
        # set_trace()
        work = cls.work_repository[f'{agent.working_on_id}']
        # set_trace()
        work.material_cost = Resources.calculate_depletion(work, agent)
        cls.products_in_progress.remove(agent.working_on_id)
        cls.on_sale_products.append(agent.working_on_id)
        work.set_status("produced")
        # reset the id of the agent
        agent.working_on_id = None

    @classmethod
    def improve_design(cls, agent, design_id):
        if design_id not in cls.realized_designs:
            raise Exception(f"{design_id} is not in realized_designs")

        # TODO: again, here improving a design means that
        # the design is taken out of the designs
        # that can be produced.
        cls.realized_designs.remove(design_id)
        cls.designs_in_progress.append(design_id)
                
        agent.working_on_id = design_id
   
    @classmethod
    def add_contribution(cls,agent):
        work = cls.work_repository[f'{agent.working_on_id}']

        work.contributors.append(agent.unique_id)
        work.hours.append(agent.worked_hours)
        work.hour_fees.append(agent.hour_fee)
        work.quality_levels.append(agent.quality_level)
        work.sustainability_levels.append(agent.sustainability_level)

    @classmethod
    def buy(cls, product_id):
        cls.on_sale_products.remove(product_id)
        cls.sold_products.append(product_id)
        work = cls.work_repository[f'{product_id}']

        # update totals
        cls.tot_contributors += len(work.contributors)
        cls.tot_hours += sum(work.hours)
        cls.tot_prices += work.get_price()
        cls.tot_quality_level += work.get_quality()
        cls.tot_sustainability_level += work.get_sustainability()
        cls.tot_material_cost += work.material_cost
        # if Resources.get_amount_resources() <= 0:
        #     breakpoint()


        
                              
    def __init__(self, id, title, img):
        self.id = id
        self.title = title
        self.img = img
        self.contributors = []
        self.hours = []
        self.hour_fees = []
        self.quality_levels = []
        self.sustainability_levels = []
        self.status = None
        self.material_cost = 0

    def get_hours(self) -> int:
        return sum(self.hours)
    
    def get_quality(self) -> float:
        quality = 0
        for i in range(len(self.hours)):
            quality = quality + self.hours[i] * (self.quality_levels[i]-(MAX_QUALITY+MIN_QUALITY)/2)

        return quality

    def get_price(self) -> float:
        """
            Price is composite of labour cost + material cost
        """
        price = 0
        # breakpoint()
        if Work.method == "producers":
            for i, id in enumerate(self.contributors):
                if agent_type(id) == "Producer":
                    price = price + self.hours[i]*self.hour_fees[i]
        elif Work.method == "equal":
            for i in range(len(self.contributors)):
                price = price + (MAX_FEE+MIN_FEE)/2
        elif Work.method == "proportional":
            for i in range(len(self.contributors)):
                price = price + self.hours[i]*self.hour_fees[i]

        price += self.material_cost
        
        return price

    def get_sustainability(self) -> float:
        # We assume that (MAX_SUS+MIN_SUS)/2 has 0 contribution to sustainability
        sustainability = 0

        for i in range(len(self.sustainability_levels)):
            sustainability = sustainability + self.hours[i]*(self.sustainability_levels[i]-(MAX_SUS+MIN_SUS)/2)

        return sustainability
    
    def set_status(self, status):
        self.status = status

    def redistribute_profit(self):
        """
            profit is labour cost only, without material cost
        """
        # breakpoint()
        if Work.method == "producers":
            for i, id in enumerate(self.contributors):
                agent = Work.model.find_agent(id)
                if agent_type(id) == "Producer":
                    agent.wealth = agent.wealth + self.hours[i]*self.hour_fees[i]
        elif Work.method == "equal":
            for i, id in enumerate(self.contributors):
                agent = Work.model.find_agent(id)
                agent.wealth = agent.wealth + (MAX_FEE+MIN_FEE)/2
        elif Work.method == "proportional":
            for i, id in enumerate(self.contributors):
                agent = Work.model.find_agent(id)
                agent.wealth = agent.wealth + self.hours[i]*self.hour_fees[i]
            
