from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Steven Monaghan'

doc = """
Voting Game
"""
class Constants(BaseConstants):
    name_in_url = 'voting_experiment_game'
    players_per_group = 4
    num_rounds = 7
    show_up_fee = 0
    conversion_rate = 0
    randlist_1 = []
    while len(randlist_1) < 3:
        rnum = random.randint(1, 3)
        if rnum not in randlist_1:
            randlist_1.append(rnum)
    randlist_2 = []
    while len(randlist_2) < 3:
        rnum = random.randint(1, 3)
        if rnum not in randlist_2:
            randlist_2.append(rnum)
    # Random payouts for player B
    b_round_payout_rand1 = random.randint(1, 3)
    b_round_payout_rand2 = random.randint(4, 6)


class Subsession(BaseSubsession):

    # Subsession level data
    rand1_id = models.PositiveIntegerField()
    rand2_id = models.PositiveIntegerField()
    rand3_id = models.PositiveIntegerField()
    round_payout_1 = models.PositiveIntegerField()
    round_payout_2 = models.PositiveIntegerField()
    round_payout_3 = models.PositiveIntegerField()
    b_round_payout_1 = models.PositiveIntegerField()
    b_round_payout_2 = models.PositiveIntegerField()

    # Subsession level functions

    def before_session_starts(self):

        # Randomize individuals into groups
        if self.round_number < 7:
            players = self.get_players()
            random.shuffle(players)

            ca1_players = [p for p in players if p.participant.vars['role'] == 'A1' and
                          p.participant.vars['treatment'] == 'alpha']
            ca2_players = [p for p in players if p.participant.vars['role'] == 'A2' and
                           p.participant.vars['treatment'] == 'alpha']
            ca3_players = [p for p in players if p.participant.vars['role'] == 'A3' and
                           p.participant.vars['treatment'] == 'alpha']
            da_players = [p for p in players if p.participant.vars['role'] == 'B' and
                          p.participant.vars['treatment'] == 'alpha']
            cb1_players = [p for p in players if p.participant.vars['role'] == 'A1' and
                          p.participant.vars['treatment'] == 'beta']
            cb2_players = [p for p in players if p.participant.vars['role'] == 'A2' and
                           p.participant.vars['treatment'] == 'beta']
            cb3_players = [p for p in players if p.participant.vars['role'] == 'A3' and
                           p.participant.vars['treatment'] == 'beta']
            db_players = [p for p in players if p.participant.vars['role'] == 'B' and
                          p.participant.vars['treatment'] == 'beta']
            group_matrix = []
            alpha_list = []
            beta_list = []

            for p in self.get_players():
                if p.participant.vars['treatment'] == 'alpha':
                    alpha_list.append(1)
                elif p.participant.vars['treatment'] == 'beta':
                    beta_list.append(1)

            while alpha_list:
                new_group_a = [
                    ca1_players.pop(),
                    ca2_players.pop(),
                    ca3_players.pop(),
                    da_players.pop()
                ]
                group_matrix.append(new_group_a)
                for i in range(0,4):
                    alpha_list.remove(1)
            while beta_list:
                new_group_b = [
                    cb1_players.pop(),
                    cb2_players.pop(),
                    cb3_players.pop(),
                    db_players.pop()
                ]
                group_matrix.append(new_group_b)
                for i in range(0,4):
                    beta_list.remove(1)
            self.set_group_matrix(group_matrix)


        # establish random sequences for player b
        self.b_round_payout_1 = Constants.b_round_payout_rand1
        self.b_round_payout_2 = Constants.b_round_payout_rand2



        # Assign A rounds in which players are payed
        self.round_payout_1 = Constants.randlist_1[0]
        self.round_payout_2= Constants.randlist_1[1]
        self.round_payout_3 = Constants.randlist_1[2]


        # Assign ID that player plays in a given round
        self.rand1_id = Constants.randlist_2[0]
        self.rand2_id = Constants.randlist_2[1]
        self.rand3_id = Constants.randlist_2[2]

        # Establish group and player parameters
        for g in self.get_groups():
            g.immoral_payoff = random.randint(0, 1)
            for p in g.get_players():
                Player.assign_id(p)
                Player.assign_vote(p)
            Group.total_vote_display(g)
            Group.payoff_outcomes(g)

    def list_pop(self,player,mylist):
            mylist.remove(player)
            return player

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
    treatment = models.CharField()
    total_vote_in_group = models.PositiveIntegerField()
    vote_to_win = models.PositiveIntegerField()
    x_payout = models.PositiveIntegerField()
    y_payout = models.PositiveIntegerField()
    total_vote_x = models.PositiveIntegerField()
    total_vote_y = models.PositiveIntegerField()
    message_space = models.CharField()
    alpha_average = models.FloatField()
    beta_average = models.FloatField()
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
        # sum up the total votes in group
        count = 0
        for p in Group.get_players(self):
            if p.id_in_round in [1,2,3]:
                count += p.vote_weight
        self.total_vote_in_group = count
        self.vote_to_win = self.total_vote_in_group//2 + 1

    def get_treatment(self):
        self.treatment = self.get_player_by_id(1).participant.vars['treatment']

    def payoff_outcomes(self):
        #assign payoff to outcome
        if self.immoral_payoff == 0:
            self.x_payout = 6
            self.y_payout = 14
        elif self.immoral_payoff == 1:
            self.x_payout = 14
            self.y_payout = 6

    def is_moral_cost(self):
        # Determine whether player voted in his own interest or the interest of decision maker
        for p in self.get_players():
            if self.immoral_payoff == 0 and p.vote == 0:
                p.individual_moral_cost = 1
            elif self.immoral_payoff == 1 and p.vote == 1:
                p.individual_moral_cost = 1
            elif self.immoral_payoff == 0 and p.vote == 1:
                p.individual_moral_cost = 0
            elif self.immoral_payoff and p.vote == 0:
                p.individual_moral_cost = 0

    def total_vote_count(self):
        #Return player votes and add up votes for option A and option B
        counter_x = []
        counter_y = []
        my_list = []
        totx = 0
        toty = 0
        for p in self.get_players():
            if p.participant.vars.get('treatment') == 'alpha' and self.subsession.round_number < 4:
                if p.id_in_round == 1:
                    my_list = Player.vote_binary(p,2,counter_x,counter_y)
                    counter_x = my_list[0]
                    counter_y = my_list[1]
                else:
                    my_list = Player.vote_binary(p, 0, counter_x, counter_y)
                    counter_x = my_list[0]
                    counter_y = my_list[1]
            elif p.participant.vars.get('treatment') == 'alpha' and self.subsession.round_number > 3:
                my_list = Player.vote_binary(p, 1, counter_x, counter_y)
                counter_x = my_list[0]
                counter_y = my_list[1]
            elif p.participant.vars.get('treatment') == 'beta' and self.subsession.round_number > 3:
                my_list = Player.vote_binary(p, 1, counter_x, counter_y)
                counter_x = my_list[0]
                counter_y = my_list[1]
            elif p.participant.vars.get('treatment') == 'beta' and self.subsession.round_number < 4:
                if p.id_in_round == 1:
                    my_list = Player.vote_binary(p, 3, counter_x, counter_y)
                    counter_x = my_list[0]
                    counter_y = my_list[1]
                elif p.id_in_round == 2 or p.id_in_round == 3:
                    my_list = Player.vote_binary(p, 2, counter_x, counter_y)
                    counter_x = my_list[0]
                    counter_y = my_list[1]
                else:
                    my_list = Player.vote_binary(p, 1, counter_x, counter_y)
                    counter_x = my_list[0]
                    counter_y = my_list[1]
        for i in counter_x:
            totx += i

        for i in counter_y:
            toty += i

        self.total_vote_x = totx
        self.total_vote_y = toty

    def make_suggestion(self):
        # Determine that group suggestion based on individual votes
        if self.get_player_by_id(1).participant.vars.get('treatment') == 'alpha' and self.round_number < 4:
            self.vote_win(4)
        elif self.get_player_by_id(1).participant.vars.get('treatment') == 'alpha' and self.round_number > 3:
            self.vote_win(3)
        elif self.get_player_by_id(1).participant.vars.get('treatment') == 'beta' and self.round_number > 3:
            self.vote_win(3)
        elif self.get_player_by_id(1).participant.vars.get('treatment') == 'beta' and self.round_number < 4:
            self.vote_win(4)

    def vote_win(self, n):
        # Determine how many votes it takes to win
        if self.total_vote_y < n:
            self.group_suggestion = 0
            self.message_space = 'Project X will earn you more money than Project Y'
        elif self.total_vote_y >= n:
            self.group_suggestion = 1
            self.message_space = 'Project Y will earn you more money than Project X'

    def set_payoffs(self):
        #Initialize payoff structure
        #Define payouts each player receives

        if self.immoral_payoff == 0 and Player.return_decision(self.get_player_by_id(4)) == 0:
            Group.pay_interior(self,6,14)
        elif self.immoral_payoff == 1 and Player.return_decision(self.get_player_by_id(4)) == 1:
            Group.pay_interior(self, 6, 14)
        elif self.immoral_payoff == 0 and Player.return_decision(self.get_player_by_id(4)) == 1:
            Group.pay_interior(self, 14, 6)
        elif self.immoral_payoff == 1 and Player.return_decision(self.get_player_by_id(4)) == 0:
            Group.pay_interior(self, 14, 6)

    def pay_interior(self,m,n):
        # Determine the payoffs for Committe and Decision Maker
        rank_list = [self.subsession.round_payout_1,self.subsession.round_payout_2,self.subsession.round_payout_3,
                     self.subsession.round_payout_1,self.subsession.round_payout_2,self.subsession.round_payout_3,]
        for p in self.get_players():
            if p.participant.vars.get('role') == "B":
                p.payout = 0
                p.payout += m
            else:
                p.payout = 0
                if p.id_in_group == rank_list[self.subsession.round_number -1]:
                    p.payout += n

    def is_group_moral_cost(self):
        if self.immoral_payoff == 0 and self.group_suggestion == 0:
            self.group_moral_cost = 1
        elif self.immoral_payoff == 1 and self.group_suggestion  == 1:
            self.group_moral_cost = 1
        elif self.immoral_payoff == 0 and self.group_suggestion  == 1:
            self.group_moral_cost = 0
        elif self.immoral_payoff == 1 and self.group_suggestion == 0:
            self.group_moral_cost = 0

    def final_payout_return(self):
        for i in self.get_players():
            x = 0
            y = 1
            for p in i.in_previous_rounds():
                x += p.in_round(y).payout
                y += 1
            if i.id_in_group != 4:
                if i.participant.vars.get('treatment') == 'alpha':
                    if (i.in_round(6).belief_average <i.group.in_round(6).alpha_average + 0.2) and (
                            i.in_round(6).belief_average> i.group.in_round(6).alpha_average - 0.2):
                            x += 6
                            p.belief_payout = 6
                    elif (i.in_round(6).belief_average <i.group.in_round(6).alpha_average + 1) and (
                          i.in_round(6).belief_average > i.group.in_round(6).alpha_average - 1):
                            x+= 2
                            p.belief_payout = 2
                    else:
                        p.belief_payout = 0
                if i.participant.vars.get('treatment') == 'beta':
                    if (i.in_round(6).belief_average <i.group.in_round(6).beta_average + 0.2) and (
                        i.in_round(6).belief_average > i.group.in_round(6).beta_average - 0.2
                    ):
                            x += 6
                            p.belief_payout = 6
                    elif (i.in_round(6).belief_average <i.group.in_round(6).beta_average + 1) and (
                          i.in_round(6).belief_average > i.group.in_round(6).beta_average - 1
                    ):
                            x+= 2
                            p.belief_payout = 2
                    else:
                        p.belief_payout = 0
            i.final_payout = x + 12
            i.final_us_payout = i.final_payout / 2





class Player(BasePlayer):
    # Player level data
    vote_weight = models.PositiveIntegerField()
    id_in_round = models.PositiveIntegerField()
    payout = models.PositiveIntegerField()
    final_payout = models.PositiveIntegerField()
    final_us_payout = models.PositiveIntegerField()
    belief_payout = models.PositiveIntegerField()
    start_time = models.FloatField()
    elapsed_time = models.FloatField()
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
    belief_average = models.DecimalField(min=0, max=10,max_digits=3,decimal_places=1)

    final_decision = models.BooleanField(
        choices=[
            [0, 'Project X'],
            [1, 'Project Y']
        ]
    )

    field = models.CharField()
    age = models.IntegerField()
    gender = models.CharField(
        choices=['Male', 'Female'],
        widget=widgets.RadioSelect(),
    )

    #Player level functions

    def assign_id(self):
        mylist_1 = [self.subsession.rand1_id,self.subsession.rand2_id,self.subsession.rand3_id,
                    self.subsession.rand1_id,self.subsession.rand2_id,self.subsession.rand3_id]
        mylist_2 = [self.subsession.rand2_id,self.subsession.rand3_id,self.subsession.rand1_id,
                    self.subsession.rand2_id,self.subsession.rand3_id,self.subsession.rand1_id]
        mylist_3 = [self.subsession.rand3_id,self.subsession.rand1_id,self.subsession.rand2_id,
                    self.subsession.rand3_id,self.subsession.rand1_id,self.subsession.rand2_id]

        if self.subsession.round_number < 7:
            if self.participant.vars.get('role') == 'A1':
                self.id_in_round = mylist_1[self.subsession.round_number - 1]
            elif self.participant.vars.get('role') == 'A2':
                self.id_in_round = mylist_2[self.subsession.round_number - 1]
            elif self.participant.vars.get('role') == 'A3':
                self.id_in_round = mylist_3[self.subsession.round_number - 1]
            elif self.participant.vars['role'] == 'B':
                self.id_in_roound = 6

    def assign_vote(self):
        if self.subsession.round_number < 6 and self.participant.vars.get('treatment') == 'alpha':
            if self.id_in_round == 1:
                self.vote_weight = 2
                self.group.fill_table_1 = 2
            elif self.id_in_round in range(2,6):
                self.vote_weight = 0
                self.group.fill_table_2 = 0
                self.group.fill_table_3 = 0
                self.group.fill_table_4 = 0
                self.group.fill_table_5 = 0
        elif 5 < self.subsession.round_number < 7 and self.participant.vars.get('treatment') == 'alpha':
            if self.id_in_round in range(1,6):
                self.vote_weight = 1
                self.group.fill_table_1 = 1
                self.group.fill_table_2 = 1
                self.group.fill_table_3 = 1
                self.group.fill_table_4 = 1
                self.group.fill_table_5 = 1
        elif 3< self.subsession.round_number < 7 and self.participant.vars.get('treatment') == 'beta':
            if self.id_in_round in range(1,4):
                self.vote_weight = 1
                self.group.fill_table_1 = 1
                self.group.fill_table_2 = 1
                self.group.fill_table_3 = 1
        elif  self.subsession.round_number < 4 and self.participant.vars.get('treatment') == 'beta':
            if self.id_in_round == 1:
                self.vote_weight = 2
                self.group.fill_table_1 = 2
            elif self.id_in_round == 2 or self.id_in_round == 3:
                self.vote_weight = 0
                self.group.fill_table_2 = 0
                self.group.fill_table_3 = 0

    def return_belief(self):
        return self.belief

    def return_decision(self):
        return self.final_decision

    def decision_for_group(self):
        self.group.g_final_decision = self.final_decision

    def vote_binary(self, n, initial,initial_2):
        # Determine how many votes are cast
        if self.id_in_round in [1,2,3]:
            if self.vote == 1:
                initial_2.append(n)
            elif self.vote == 0:
                initial.append(n)
        return [initial, initial_2]

    def followed(self):
        # Find the number of times that they followed
        alpha_list = []
        beta_list = []
        for p in self.subsession.get_players():
            if p.id_in_group == 4:
                if p.participant.vars.get('treatment') == 'alpha':
                    for i in range(1,4):
                        if p.group.in_round(i).group_suggestion == p.group.in_round(i).g_final_decision:
                            alpha_list.append(1)
                        elif p.group.in_round(i).group_suggestion != p.group.in_round(i).g_final_decision:
                            alpha_list.append(0)
                if p.participant.vars.get('treatment') == 'beta':
                    for i in range(1,4):
                        if p.group.in_round(i).group_suggestion == p.group.in_round(i).g_final_decision:
                            beta_list.append(1)
                        elif p.group.in_round(i).group_suggestion != p.group.in_round(i).g_final_decision:
                            beta_list.append(0)

        # Calculate the average number of times
        alpha_counter = 0
        beta_counter = 0
        for i in alpha_list:
            alpha_counter += i
        for i in beta_list:
            beta_counter += i
        self.alpha_average = (alpha_counter/20)*4
        self.beta_average = (beta_counter/20)*4
