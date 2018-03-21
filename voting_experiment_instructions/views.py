from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import time


class Screen_2_A(Page):
    def is_displayed(self):
        player_id_list = [x * 4 for x in range(0, 12)]
        if self.player.id_in_group not in player_id_list:
            return self.player

class Screen_2_B(Page):

    def is_displayed(self):
        player_id_list = [x * 4 for x in range(0, 12)]
        if self.player.id_in_group in player_id_list:
            return self.player


class Screen_3_A(Page):
    def is_displayed(self):
        player_id_list = [x * 4 for x in range(0, 12)]
        if self.player.id_in_group not in player_id_list:
            return self.player


class Screen_3_B(Page):

    def is_displayed(self):
        player_id_list = [x * 4 for x in range(0, 12)]
        if self.player.id_in_group in player_id_list:
            return self.player


class Screen_4_A(Page):
    def is_displayed(self):
        player_id_list = [x * 4 for x in range(0, 12)]
        if self.player.id_in_group not in player_id_list:
            return self.player

    def vars_for_template(self):
        return {'my_image': "voting_experiment_instructions/instructions_1.JPG"}

class Screen_4_B_instructions(Page):
    def is_displayed(self):
        player_id_list = [x * 4 for x in range(0, 12)]
        if self.player.id_in_group in player_id_list:
            return self.player

class Screen_5_A(Page):
    def is_displayed(self):
        player_id_list = [x * 4 for x in range(0, 12)]
        if self.player.id_in_group not in player_id_list:
            return self.player

class Screen_5_B_instructions(Page):
    def is_displayed(self):
        player_id_list = [x * 4 for x in range(0, 12)]
        if self.player.id_in_group in player_id_list:
            return self.player


class Section_6_A(Page):
    def is_displayed(self):
        player_id_list = [x * 4 for x in range(0, 12)]
        if self.player.id_in_group not in player_id_list:
            return self.player

    def vars_for_template(self):
        return {'my_image': 'voting_experiment_instructions/instructions_2.JPG',
                'my_image_2': 'voting_experiment_instructions/instructions_3.JPG',
                'my_image_3': 'voting_experiment_instructions/instructions_4.JPG',
                'my_image_4': 'voting_experiment_instructions/instructions_5.JPG'}


class Comprehenstion_1(Page):
    def is_displayed(self):
        player_id_list = [x * 4 for x in range(0, 12)]
        if self.player.id_in_group not in player_id_list:
            return self.player

    def vars_for_template(self):
        return {'my_image': "voting_experiment_instructions/comprehension_1.JPG"}
    form_model = models.Player
    form_fields = ['q_1','q_2','q_3']

    def error_message(self,values):
        wrong = False
        if values['q_1'] != "Project Y":
            self.player.num_wrong += 1
            wrong = True
        if values['q_2'] != "E$12":
            self.player.num_wrong += 1
            wrong = True
        if values['q_3'] != "Project X":
            self.player.num_wrong += 1
            wrong = True
        if wrong == True:
            return 'You have chosen one or more wrong answers. Please read the question again and try to answer once more'

class Comprehension_2(Page):

    def is_displayed(self):
        player_id_list = [x * 4 for x in range(0, 12)]
        if self.player.id_in_group not in player_id_list:
            return self.player
    form_model = models.Player
    form_fields = ['q_4']

    def error_message(self, values):
        wrong = False
        if values['q_4'] != True:
            self.player.num_wrong += 1
            wrong = True

        if wrong == True:
            return 'You have chosen the wrong answer. Please read the question again and try to answer once more'

class Comprehension_3(Page):
    def is_displayed(self):
        player_id_list = [x * 4 for x in range(0, 12)]
        if self.player.id_in_group not in player_id_list:
            return self.player
    def vars_for_template(self):
        return {'my_image': "voting_experiment_instructions/comprehension_3.JPG"}
    form_model = models.Player
    form_fields = ['q_5', "q_6"]

    def error_message(self,values):
        wrong = False
        if values['q_5'] != 'Message X: “Project X will earn you more money than Project Y"':
            self.player.num_wrong += 1
            wrong = True
        if values['q_6'] != 'Message Y: “Project Y will earn you more money than Project X”':
            self.player.num_wrong += 1
            wrong = True

        if wrong == True:
            return 'You have chosen one or more wrong answers. Please read the question again and try to answer once more'

class Comprehension_4(Page):
    def is_displayed(self):
        player_id_list = [x * 4 for x in range(0, 12)]
        if self.player.id_in_group not in player_id_list:
            return self.player
    def vars_for_template(self):
        return {'my_image': "voting_experiment_instructions/comprehension_4.JPG"}
    form_model = models.Player
    form_fields = ['q_7', "q_8"]

    def error_message(self,values):
        wrong = False

        if values['q_7'] != 'Message X: “Project X will earn you more money than Project Y"':
            self.player.num_wrong += 1
            wrong = True

        if values['q_8'] != 'Message X: “Project X will earn you more money than Project Y"':
            self.player.num_wrong += 1
            wrong = True

        if wrong == True:
            return 'You have chosen one or more wrong answers. Please read the question again and try to answer once more'

class Comprehension_5(Page):

    form_model = models.Player
    form_fields = ['q_9']

    def is_displayed(self):
        player_id_list = [x * 4 for x in range(0, 12)]
        if self.player.id_in_group not in player_id_list:
            return self.player

    def error_message(self,values):
        wrong = False

        if values['q_9'] != 'True':
            self.player.num_wrong += 1
            wrong = True

        if wrong == True:
            return ' You have chosen one or more wrong answers. Please read the question again and try to answer once more.'

class Comprehension_6(Page):

    form_model = models.Player
    form_fields = ['q_10']

    def is_displayed(self):
        player_id_list = [x * 4 for x in range(0, 12)]
        if self.player.id_in_group not in player_id_list:
            return self.player

    def error_message(self, values):
        wrong = False

        if values['q_10'] != '''The decision that you make, the decisions that other participants make, and who among the three Type A participants in a given round is randomly selected to earn the money that is associated with the project that the Type B participant chose to implement''':
            self.player.num_wrong += 1
            wrong = True

        if wrong == True:
            return ' You have chosen one or more wrong answers. Please read the question again and try to answer once more.'

class Post_Instruction_Page(WaitPage):
    def after_all_players_arrive(self):
        pass


page_sequence = [

    ]

'''
    Screen_2_A,
    Screen_2_B,
    Screen_3_A,
    Screen_3_B,
    Screen_4_A,
    Screen_5_A,
    Section_6_A,
    Comprehenstion_1,
    Comprehension_2,
    Comprehension_3,
    Comprehension_4,
    Comprehension_6,
    Comprehension_5,
    Post_Instruction_Page
'''
