from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
import math
from ast import literal_eval
author = 'Steven Monaghan'

doc = """
Voting Game
"""

class Constants(BaseConstants):
    name_in_url = 'voting_experiment_game'
    players_per_group = 4
    num_rounds = 19
    show_up_fee = 0
    conversion_rate = 0



class Subsession(BaseSubsession):

    players_payoff = models.CharField()
    players_id = models.CharField()
    round_order = models.CharField()

    def before_session_starts(self):
        """Assign variables before experiment starts"""

        # Randomize individuals into groups
        if self.round_number < Constants.num_rounds:
            players = self.get_players()
            random.shuffle(players)

            ca1_players = [p for p in players if p.participant.vars['role'] == 1]
            ca2_players = [p for p in players if p.participant.vars['role'] == 2]
            ca3_players = [p for p in players if p.participant.vars['role'] == 3]
            da_players = [p for p in players if p.participant.vars['role'] == 4]
            group_matrix = []

            while ca1_players:
                new_group = [
                    ca1_players.pop(),
                    ca2_players.pop(),
                    ca3_players.pop(),
                    da_players.pop()
                ]
                group_matrix.append(new_group)
            self.set_group_matrix(group_matrix)

        # Establish group and player parameters
        if self.round_number == 1:
            group_payoff_rounds = self.set_payoff_rounds()
            group_id_rounds = self.set_id_rounds()
        self.gen_round_order()
        round_list = self.gen_round_list()
        round_order = literal_eval(self.round_order)
        for g in self.get_groups():
            g.immoral_payoff = random.randint(0, 1)
            g.equal_round = False
            if round_order[self.round_number - 1] == 1 or \
               round_order[self.round_number  - 1] == 3:
               g.immoral_payoff = 2
               g.equal_round = True
            if self.round_number == 1:
                self.players_payoff = str(group_payoff_rounds)
                self.players_id = str(group_id_rounds)
            else:
                self.players_payoff = self.in_round(1).players_payoff
                self.players_id = self.in_round(1).players_id
            for p in g.get_players():
                if self.round_number < Constants.num_rounds:
                    p.assign_id(literal_eval(self.players_id),self.round_number - 1)
                    p.assign_payoff(literal_eval(self.players_payoff),
                    round_list,self.round_number - 1)
                p.assign_vote(self.round_number,round_order)
            g.total_vote_display()
            g.payoff_outcomes()

    def set_payoff_rounds(self):
        """Assign player payoff rounds for game"""
        if self.round_number == 1:
            group_value_list = [[1,2,3],[4,5,6],[7,8,9],[10,11,12],
                                [13,14,15],[16,17,18]]
            player_payoff = {}
            for player in [1,2,3,4]:
                player_list = []
                if player == 4:
                    group_value_list = [i for i in range(1,19)]
                    # Participant B players are assigned random round in each 6
                    for i in group_value_list:
                        player_list.append(i)
                    player_payoff['player_4'] = player_list
                else:
                    # Particpant A players are assigned values from group values list
                    for i in range(6):
                        player_payoff['player_{}'.format(player)] = player_list
                        val = random.choice(group_value_list[i])
                        player_list.append(val)
                        group_value_list[i].remove(val)
            return player_payoff

    def set_id_rounds(self):
        player_id = {}
        if self.round_number == 1:
            group_value_list = [[1,2,3] for i in range(18)]
            for player in [1,2,3,4]:
                id_list = []
                if player == 4:
                    id_list = [4 for i in range(18)]
                    player_id['player_4'] = id_list
                elif player < 4 :
                    for i in range(18):
                        val = random.choice(group_value_list[i])
                        id_list.append(val)
                        group_value_list[i].remove(val)
                player_id['player_{}'.format(player)] = id_list

            return player_id
    def gen_round_list(self):
        """Generate index for each of the rounds in the game"""
        my_list = []

        for i in range(1,Constants.num_rounds):
            if i < 4:
                my_list.append(0)
            elif i > 3 and i < 7:
                my_list.append(1)
            elif i > 6 and i <10:
                my_list.append(2)
            elif i > 9 and i < 13:
                my_list.append(3)
            elif i > 12 and i < 16:
                my_list.append(4)
            elif i > 15 and i < Constants.num_rounds:
                my_list.append(5)
            else:
                pass
        return my_list

    def gen_round_order(self):
        """
        Function generates the rounds that each group will play with
        in the game
        """
        if self.round_number == 1:
            round_list = [0,0,0,0,0,0,1,1,1,2,2,2,2,2,2,3,3,3]
            random.shuffle(round_list)
            round_list.append(99)
            self.round_order = str(round_list)
        else:
            self.round_order = self.in_round(1).round_order

class Group(BaseGroup):
    # Group level data
    immoral_payoff = models.BooleanField(
        choices = [
            [0,'X'],
            [1,'Y']
        ]
    )
    group_suggestion = models.BooleanField(
        choices=[
            [0, 'Project X'],
            [1, 'Project Y']
        ]
    )
    fill_table_1 = models.CharField()
    fill_table_2 = models.CharField()
    fill_table_3 = models.CharField()
    total_vote_in_group = models.PositiveIntegerField()
    vote_to_win = models.PositiveIntegerField()
    x_payout = models.PositiveIntegerField()
    y_payout = models.PositiveIntegerField()
    total_vote_x = models.PositiveIntegerField()
    total_vote_y = models.PositiveIntegerField()

    message_space = models.CharField()
    alpha_average = models.FloatField()
    equal_round = models.BooleanField()
    group_moral_cost = models.BooleanField(
        choices = [
            [0, 'No'],
            [1, 'Yes']
        ]
    )
    g_final_decision = models.BooleanField(
            choices = [[0, 'Project X'],
                      [1, 'Project Y']]
    )
    #Group level functions

    def total_vote_display(self):
        """sum up the total votes in group"""
        count = 0
        for p in self.get_players():
            if p.id_in_round in [1,2,3]:
                count += p.vote_weight
        self.total_vote_in_group = count
        self.vote_to_win = self.total_vote_in_group//2 + 1

    def total_vote_count(self,round_order):
        """Determine which of the options wins contingent on the votes cast"""

        total_x = 0
        total_y = 0
        round_order = literal_eval(round_order)
        round_order = round_order[self.round_number - 1]

        if round_order == 0 or round_order == 1:
            for player in self.get_players():
                if player.vote == 0:
                    total_x += 1
                elif player.vote == 1:
                    total_y += 1
        elif round_order == 2 or round_order == 3:
            for player in self.get_players():
                if player.id_in_round == 1:
                    if player.vote == 0:
                        total_x += 2
                    elif player.vote == 1:
                        total_y += 2
                else:
                    if player.vote == 0:
                        total_x += 0
                    elif player.vote == 1:
                        total_y += 0

        if total_y >= self.vote_to_win:
            self.message_space = "Project Y will earn you more money than Project X"
            self.group_suggestion = 1
        else:
            self.message_space = "Project X will earn you more money than Project Y"
            self.group_suggestion = 0

        self.total_vote_x = total_x
        self.total_vote_y = total_y

    def payoff_outcomes(self):
        """assign payoff to outcome"""
        if self.immoral_payoff == 0:
            self.x_payout = 4
            self.y_payout = 16
        elif self.immoral_payoff == 1:
            self.x_payout = 16
            self.y_payout = 4
        elif self.immoral_payoff == 2:
            rand_num = random.randint(0,1)
            if rand_num == 0:
                self.x_payout = 16
                self.y_payout = 8
            elif rand_num == 1:
                self.x_payout = 8
                self.y_payout = 16


    def set_payoffs(self):
        """Set player payoffs for round"""
        for player in self.get_players():
            if self.g_final_decision == 0:
                if player.id_in_group < 4:
                    player.payout = self.x_payout
                else:
                    player.payout = self.y_payout
            elif self.g_final_decision == 1:
                if player.id_in_group < 4:
                    player.payout = self.y_payout
                else:
                    player.payout = self.x_payout



    def set_add_payoffs(self):
        """Add players payoff from bonus question"""
        for player in self.get_players():
            if player.participant.vars['role'] == 4:
                pass
            else:
                if player.belief_average < self.alpha_average + .02 and player.belief_average > self.alpha_average - .02:
                    player.belief_payout = 18
                elif player.belief_average < self.alpha_average + 1 and player.belief_average > self.alpha_average -1:
                    player.belief_payout = 6
                else:
                    player.belief_payout = 0


    def make_sugestion(self):
        """Make suggestion on the basis of group vote"""

        # Collect the player votes
        for player in self.get_players():
            vote_count += player.vote
        # If player votes are greater than two send y message
        if vote_count >= 2:
            self.message_space = "Project Y"
            self.group_suggestion = 1
        elif vote_count < 2:
            self.message_space = "Project X"
            self.group_suggestion = 0

    def is_moral_cost(self):
        """Determine if the suggestion moral or immoral"""

        if self.x_payout > self.y_payout:
            project = 0
            if self.message_space == "Project X":
                self.group_moral_cost = 1
            elif self.message_space == "Project Y":
                self.group_moral_cost = 0
        elif self.y_payout > self.x_payout:
            project = 1
            if self.message_space == "Project X":
                self.group_moral_cost = 0
            elif self.message_space == "Project Y":
                self.group_moral_cost = 1

        for player in self.get_players():
            player.is_ind_moral_cost(project)

    def final_payout_return(self):
        """
           Calculate the final payoff for the player. Only Add
           the rounds in which they are assigned to recieve a
           payoff
        """

        for player in self.get_players():
            payout_sum = 0
            for p in player.in_previous_rounds():
                if p.payoff_rounds:
                    payout_sum += p.payout
            if player.id_in_group < 4:
                payout_sum += player.in_round(18).belief_payout

            player.final_payout = payout_sum
            player.final_us_payout = math.ceil(payout_sum/6)

    def followed(self):
        """Find the number of times that they followed the group message"""
        alpha_list = []
        for p in self.get_players():
            if p.id_in_group == 4:
                for i in range(1,4):
                    if p.group.in_round(i).group_suggestion == p.group.in_round(i).g_final_decision:
                        alpha_list.append(1)
                    elif p.group.in_round(i).group_suggestion != p.group.in_round(i).g_final_decision:
                        alpha_list.append(0)

        # Calculate the average number of times
        alpha_counter = 0
        for i in alpha_list:
            alpha_counter += i
        self.alpha_average = alpha_counter


class Player(BasePlayer):
    # Player level data
    vote_weight = models.PositiveIntegerField()
    id_in_round = models.PositiveIntegerField()
    payout = models.PositiveIntegerField()
    payoff_rounds = models.BooleanField()
    final_payout = models.PositiveIntegerField()
    final_us_payout = models.PositiveIntegerField()
    belief_payout = models.PositiveIntegerField()
    individual_moral_cost = models.BooleanField(
     choices =[
                [0,'No'],
                [1,'Yes']
        ]
    )
    vote = models.BooleanField(
        choices = [
            [0, 'Project X will earn you more money than project Y'],
            [1, 'Project Y will earn you more money than project X']
        ]
    )

    belief = models.BooleanField(
        choices=[
            [0, 'No'],
            [1, 'Yes']
        ]
    )
    belief_average = models.DecimalField(min=0, max=18,max_digits=3,decimal_places=1)

    final_decision = models.BooleanField(
        choices=[
            [0, 'Project X'],
            [1, 'Project Y']
        ]
    )

    field = models.CharField()
    age = models.IntegerField(min=18,max=100)
    gender = models.CharField(
        choices=['Male', 'Female'],
        widget=widgets.RadioSelect(),
    )


    def assign_id(self,player_id,round_number):
        """Assign players rounds in which they are assigned id's"""
        if self.subsession.round_number < Constants.num_rounds:
            if self.participant.vars.get('role') == 4:
                self.id_in_round = 4
            else:
                self.id_in_round = player_id['player_{}'.format(
                self.participant.vars['role']
                )][round_number]

    def assign_payoff(self,player_payoff,round_list,round_number):
        """Assign players rounds in which they are payed off"""
        if self.subsession.round_number < Constants.num_rounds:
            if self.subsession.round_number == player_payoff['player_{}'.format(
            self.participant.vars['role'])][round_list[round_number]]:
                self.payoff_rounds = True
            else:
                self.payoff_rounds = False

    def assign_vote(self, round_number,round_order):
        if round_order[round_number - 1] == 0 or round_order[round_number-1] == 1:
            self.vote_weight = 1
            self.group.fill_table_1 = 1
            self.group.fill_table_2 = 1
            self.group.fill_table_3 = 1
        elif round_order[round_number-1] == 2 or round_order[round_number-1] ==3:
            if self.id_in_round == 1:
                self.vote_weight = 2
            else:
                self.vote_weight = 0

            self.group.fill_table_1 = 2
            self.group.fill_table_2 = 0
            self.group.fill_table_3 = 0

    def return_belief(self):
        return self.belief

    def return_decision(self):
        return self.final_decision

    def decision_for_group(self):
        self.group.g_final_decision = self.final_decision

    def is_ind_moral_cost(self, project):
        """Determine if player voted morally or not"""
        if project == 0:
            if self.vote == 1:
                self.individual_moral_cost = 1
            elif self.vote == 0:
                self.individual_moral_cost = 0
        elif project == 1:
            if self.vote == 1:
                self.individual_moral_cost = 0
            elif self.vote == 0:
                self.individual_moral_cost = 1
