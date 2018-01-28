from openravepy import *
import openravepy
import random
from numpy import *

class Box(object):
    def __init__(self):
       self.lower_y = -0.4202331
       self.upper_y = -0.0103842

       self.second_col = 0.26268633
       self.third_col = 0.30568633

       self.second_row = 0.26855474
       self.third_row = 0.22959245
       self.forth_row = 0.22868633

       self.objects = []

    def random_pose(self):
        x = random.uniform(self.lower_x, self.upper_x)
        y = random.uniform(self.lower_y, self.upper_y)

        transform = numpy.identity(4)
        transform[0, 3] = x
        transform[1, 3] = y
        transform[2, 3] = self.z

        return transform

class Box_J(Box):
    def __init__(self, initial_x, initial_z):
        super(Box_J, self).__init__()
        self.lower_x = initial_x
        self.upper_x = self.lower_x + 0.25
        self.z = initial_z

class Box_G(Box_J):
    def __init__(self, initial_x, initial_z):
        super(Box_G, self).__init__(initial_x, initial_z)
        self.z += self.second_row

class Box_D(Box_G):
    def __init__(self, initial_x, initial_z):
        super(Box_D, self).__init__(initial_x, initial_z)
        self.z += self.third_row

class Box_A(Box_D):
    def __init__(self, initial_x, initial_z):
        super(Box_A, self).__init__(initial_x, initial_z)
        self.z += self.forth_row

class Box_K(Box_J):
    def __init__(self, initial_x, initial_z):
        super(Box_K, self).__init__(initial_x, initial_z)
        self.lower_x += self.second_col

class Box_H(Box_K):
    def __init__(self, initial_x, initial_z):
        super(Box_H, self).__init__(initial_x, initial_z)
        self.z += self.second_row

class Box_E(Box_H):
    def __init__(self, initial_x, initial_z):
        super(Box_E, self).__init__(initial_x, initial_z)
        self.z += self.third_row

class Box_B(Box_E):
    def __init__(self, initial_x, initial_z):
        super(Box_B, self).__init__(initial_x, initial_z)
        self.z += self.forth_row

class Box_L(Box_K):
    def __init__(self, initial_x, initial_z):
        super(Box_L, self).__init__(initial_x, initial_z)
        self.lower_x += self.third_col

class Box_I(Box_L):
    def __init__(self, initial_x, initial_z):
        super(Box_I, self).__init__(initial_x, initial_z)
        self.z += self.second_col

class Box_F(Box_I):
    def __init__(self, initial_x, initial_z):
        super(Box_F, self).__init__(initial_x, initial_z)
        self.z += self.third_col

class Box_C(Box_F):
    def __init__(self, initial_x, initial_z):
        super(Box_C, self).__init__(initial_x, initial_z)
        self.z += self.forth_row


class Utilities:
    def __init__(self):
        self.env = Environment()
        self.env.SetViewer('qtcoin')
        self.env.Load('amazon_picking_challenge_env.xml')



        self.amazon_objects_names = [  "champion_copper_plus_spark_plug",          "cheezit_big_original",
                                        "crayola_64_ct",                            #"dove_beauty_bar",
        #                                # "dr_browns_bottle_brush",                   "elmers_washable_no_run_school_glue",
        #                                # "expo_dry_erase_board_eraser",              "feline_greenies_dental_treats",
        #                                # "first_years_take_and_toss_straw_cups",     "genuine_joe_plastic_stir_sticks",
        #                                # "highland_6539_self_stick_notes",           "kong_air_dog_squeakair_tennis_ball",
        #                                # "kong_duck_dog_toy",                        "kong_sitting_frog_dog_toy",
        #                                # "laugh_out_loud_joke_book",                 "kygen_squeakin_eggs_plush_puppies",
        #                                # "mark_twain_huckleberry_finn",              "mead_index_cards",
        #                                # "mommys_helper_outlet_plugs",               "munchkin_white_hot_duck_bath_toy",
        #                                # "one_with_nature_soap_dead_sea_mud",        "oreo_mega_stuf",
        #                                # "paper_mate_12_count_mirado_black_warrior", "rollodex_mesh_collection_jumbo_pencil_cup",
        #                                # "safety_works_safety_glasses",              "sharpie_accent_tank_style_highlighters",
        #                                # "stanley_66_052"
                                     ]

        self.amazon_objects = map(self.env.GetKinBody, self.amazon_objects_names)
        random.shuffle(self.amazon_objects)
        self.shelf = self.env.GetKinBody("kiva_pod")
        initial_x = self.shelf.GetTransform()[0][3]
        initial_z = self.shelf.GetTransform()[2][3]

        self.box_a = Box_A(initial_x, initial_z)
        self.box_b = Box_B(initial_x, initial_z)
        self.box_c = Box_C(initial_x, initial_z)
        self.box_d = Box_D(initial_x, initial_z)
        self.box_e = Box_E(initial_x, initial_z)
        self.box_f = Box_F(initial_x, initial_z)
        self.box_g = Box_G(initial_x, initial_z)
        self.box_h = Box_H(initial_x, initial_z)
        self.box_i = Box_I(initial_x, initial_z)
        self.box_j = Box_J(initial_x, initial_z)
        self.box_k = Box_K(initial_x, initial_z)
        self.box_l = Box_L(initial_x, initial_z)

        self.boxes = [self.box_a, self.box_b, self.box_c, self.box_d, self.box_e,
                      self.box_f, self.box_g, self.box_h, self.box_i, self.box_j,
                      self.box_k, self.box_l]

        random.shuffle(self.boxes)

        box_index = 0
        for amazon_object in self.amazon_objects:
            box = self.boxes[box_index]
            box.objects.append(amazon_object)
            box_index += 1

            if box_index > len(self.boxes):
                box_index = 0

            transform = box.random_pose()
            amazon_object.SetTransform(transform)

            while self.env.CheckCollision(amazon_object, self.shelf) and any(map(self.env.CheckCollision, box.objects)):
                transform[0, 3] += random.choice([0.01, -0.01])
                transform[1, 3] += random.choice([0.01, -0.01])
                amazon_object.SetTransform(transform)

utilities = Utilities()
