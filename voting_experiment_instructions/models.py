from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
author = 'Steven Monaghan'

doc = """
Voting instructions
"""


class Constants(BaseConstants):
    name_in_url = 'voting_experiment_instructions'
    players_per_group = 4
    num_rounds = 1
    show_up_fee = 5
    conversion_rate = 0.5
    POINTS_CUSTOM_NAME = 'E$'

    it2A = 'voting_experiment_instructions/Screen_2_A_instructions.html'
    it2B = 'voting_experiment_instructions/Screen_2_B_instructions.html'
    it3A = 'voting_experiment_instructions/Screen_3_A_instructions.html'
    it3B = 'voting_experiment_instructions/Screen_3_B_instructions.html'
    it4A = 'voting_experiment_instructions/Screen_4_A_Instructions.html'
    it4B = 'voting_experiment_instructions/Screen_4_B_instructions.html'
    it5A = 'voting_experiment_instructions/Screen_5_A_instructions.html'
    it6A = 'voting_experiment_instructions/Section_6_A_instructions.html'


class Subsession(BaseSubsession):
    def before_session_starts(self):

        'Define if player is a type A or type B player'
        for g in self.get_groups():
            g.get_player_by_id(1).participant.vars['role'] = 1
            g.get_player_by_id(2).participant.vars['role'] = 2
            g.get_player_by_id(3).participant.vars['role'] = 3
            g.get_player_by_id(4).participant.vars['role'] = 4

class Group(BaseGroup):
    pass


class Player(BasePlayer):

    q_1 = models.CharField(
        choices = ['Project X',
                   'Project Y']
    )
    q_2 = models.CharField(
        choices=['E$15',
                 'E$8',
                 'E$12',
                 'E$7']
    )
    q_3 = models.CharField(
        choices = ['Project X',
                   'Project Y']
        )
    q_4 = models.CharField(
        choices = ['in three rounds',
                   'the number is random',
                   'in all 18 rounds',
                   'in one round']
    )
    q_5 = models.CharField(
        choices = ['Message X: “Project X will earn you more money than Project Y"',
                   'Message Y: “Project Y will earn you more money than Project X”']
    )
    q_6 = models.CharField(
        choices = ['Message X: “Project X will earn you more money than Project Y"',
                   'Message Y: “Project Y will earn you more money than Project X”']
    )
    q_7 = models.CharField(
        choices=['Message X: “Project X will earn you more money than Project Y"',
                 'Message Y: “Project Y will earn you more money than Project X”']
    )
    q_8 = models.CharField(
        choices=['Message X: “Project X will earn you more money than Project Y"',
                 'Message Y: “Project Y will earn you more money than Project X"']
    )
    q_9 = models.CharField(
    choices=['False','True']
    )
    q_10 = models.CharField(
    widget=widgets.RadioSelect,
    choices = [
        'Only the decision that you make',
        'Only the decisions that other participants make',
        'The decision that you make, the decisions that other participants make, and who among the three Type A participants in a given round is randomly selected to earn the money that is associated with the project that the Type B participant chose to implement']
    )
    num_wrong = models.IntegerField(initial=0)
    time_spent = models.FloatField()
