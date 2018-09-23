from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer
)
import random
import numpy as np
from ast import literal_eval
author = 'Steven Monaghan'

doc = """
Voting Game
"""


class Constants(BaseConstants):
    name_in_url = 'voting_experiment_game'
    players_per_group = 6
    num_rounds = 31
    show_up_fee = 0
    conversion_rate = 0
    treatments = 3
    treatment_dict = '{}'
    players_id = '{}'
    round_order = '[]'
    group_id_rounds = '{}'
    group_payoff_rounds = '{}'
    group_conflict_rounds = '[]'
    tracker_dict = '{}'


class Subsession(BaseSubsession):

    def before_session_starts(self):
        """Assign variables before experiment starts"""

        self.randomize_players()
        self.establish_groups()
        self.establish_parameters()

    def randomize_players(self):
        """
        Randomize the players for each round
        """
        # If round == 1 then set payoffs
        if self.round_number == 1:
            self.gen_payment_rounds()

        self.assign_player_payoff_rounds()
        if self.round_number < Constants.num_rounds:
            players = self.get_players()
            random.shuffle(players)

            players_dict = {'player_{}': [] for i in range(1, Constants.players_per_group + 1)}
            for player in players:
                players_dict['player_{}'.format(player.participant.vars['role'])].append(player)

        Constants.players_id = str(players_dict)

    def establish_groups(self):
        """
        Establish groups for each round in the game
        """
        players_dict = literal_eval(Constants.players_id)
        group_matrix = []
        while players_dict['player_1']:
            new_group = [players_dict['player_{}'.format(i)].pop() for i in range(1, Constants.players_per_group + 1)]
            group_matrix.append(new_group)

        self.set_group_matrix(group_matrix)

    def establish_parameters(self):

        # Establish group and player parameters
        if self.round_number == 1:
            self.parameters_for_game()

        for group in self.get_groups():
            group.assign_rounds()
            group.assign_payoff_rounds()
            group.assign_vote_weight
            group.conflict_round()
            group.assign_vote_to_win()
            group.immoral_payoff = random.randint(0, 1)
            group.assign_relative_payouts()

    def parameters_for_game(self):
        self.set_payoff_rounds()
        self.gen_round_order()
        self.gen_tracker_dict()
        self.set_id_rounds()
        self.set_conflict_rounds()

    def set_treatments(self):
        """
        Define treatments for the game.
        """

        treatment_dict = literal_eval(Constants.treatment_dict)
        for i in range(1, Constants.treatments + 1):
            if i == 1:
                treatment_dict['treatment_1'] = {'votes': [2, 2, 1, 1, 1], 'quota': 5,
                                                 'high': 4,  'conflict': 3, 'num_high': 2}
            elif i == 2:
                treatment_dict['treatment_2'] = {'votes': [3, 1, 1, 1, 1], 'quota': 4,
                                                 'high': 2, 'conflict': 10, 'num_high': 1}
            elif i == 3:
                treatment_dict['treatment_3'] = {'votes': [1, 1, 1, 1, 1], 'quota': 3,
                                                 'high': 10, 'conflict': 5, 'num_high': 5}

        Constants.treatment_dict = str(treatment_dict)

    def gen_round_order(self):
        """
        Function generates the rounds that each group will play with
        in the game
        """

        round_order = [i for i in range(1, Constants.treatments + 1)] * int(
            ((Constants.num_rounds - 1)/Constants.treatments))
        random.shuffle(round_order)

        Constants.round_order = str(round_order)


    def gen_payment_rounds(self):
        """
        Generates the rounds in which payers are paid on for each player
        """
        payoff_dict = literal_eval(Constants.group_payoff_rounds)

        for index, player in enumerate(self.get_players):
            index += 1
            if player.id_in_group == 6:
                payoff_dict['player_{}'.format(index)] = [i for i in range(1, Constants.num_rounds)]
            else:
                payoff_list = []
                while len(payoff_list) != 6:
                    rand_num = random.randint(1, 31)
                    if rand_num not in payoff_list:
                        payoff_list.append(random.randint(rand_num))

        Constants.group_payoff_rounds = str(payoff_dict)

    def assign_player_payoff_rounds(self):
        """
        If round number is equal to the to the number contained in the payoff dictionary
        set the players payoff for the round to true.
        """
        payoff_dict = literal_eval(Constants.group_payoff_rounds)

        for index, player in enumerate(self.get_players()):
            index += 1
            payoff_list = payoff_dict['player_{}'.format(index)]
            if self.round_number in payoff_list:
                player.payoff_rounds = True
            else:
                player.payoff_rounds = False

    def gen_tracker_dict(self):
        """
        Generate a dictionary that is used to track player assignment to rounds
        """

        tracker_dict = literal_eval(Constants.tracker_dict)
        for player in range(1, Constants.players_per_group + 1):
            tracker_dict['player_{}'.format(player)] = {}

        for value in tracker_dict.values():
            for treatment in range(1, Constants.treatments):
                value['treatment_{}'.format(treatment)]['id'] = [None for i in range(Constants.num_rounds)]
                value['treatment_{}'.format(treatment)]['payoff'] = [None for i in range(Constants.num_rounds)]

        Constants.tracker_dict = str(tracker_dict)


    def set_conflict_rounds(self):
        """
        Determine which rounds there is a competing payoff and in which rounds there is an equal payoff
        """
        round_order = literal_eval(self.round_order)
        treatment_dict = literal_eval(self.treatment_dict)
        conflict_rounds = []
        conflict_tracker = {'treatment_{}'.format(i): 0 for i in range(1, Constants.treatments + 1)}

        for cur_round in round_order:
            if conflict_tracker['treatment_{}'.format(cur_round)] >= treatment_dict['treatment_{}'.format(
                    cur_round)]['conflict']:
                conflict_rounds.append(False)
            else:
                result = self.check_lower_bound(cur_round, conflict_tracker['treatment_{}'.format(cur_round)])
                conflict_rounds.append(result)
                conflict_tracker['treatment_{}'.format(cur_round)] += result

        Constants.conflict_rounds = str(conflict_rounds)

    def set_id_rounds(self):
        """
        Define each players id in the group for each round in the game
        """
        tracker_dict = literal_eval(Constants.tracker_dict)
        round_order = literal_eval(Constants.round_order)

        for i, current_round in enumerate(round_order):
            check = False
            while not check:
                sample_list = [i for i in range(1, Constants.players_per_group)]
                for player_num in range(1, Constants.players_per_group):
                    sample = np.random.choice(sample_list, replace=False)
                    tracker_dict['player_{}'.format(player_num)]['treatment_{}'.format(current_round)]['id'][i] = sample

                check = self.check_max_id_condition(current_round, tracker_dict)
            tracker_dict['player_{}'.format(
                Constants.players_per_group)]['treatment_{}'.format(
                    current_round)]['id'][i] = Constants.players_per_group

        Constants.tracker_dict = str(tracker_dict)

    def check_max_id_condition(self, current_round, tracker_dict):
        """
        Check to make sure that players have not been assigned to the max position in round list more than the times
        that they are allowed to occupy that position.
        """
        treatment_dict = literal_eval(Constants.treatment_dict)
        num_high = treatment_dict['treatment_{}'.format(current_round)]['num_high']
        rounds_high = treatment_dict['treatment_{}'.format(current_round)]['rounds_high']

        check = False
        for player_num in range(1, Constants.players_per_group):
            count_list = tracker_dict['player_{}'.format(player_num)]['treatment_{}'.format(current_round)]['id']

            count = 0
            for player_id in count_list:
                if player_id in range(1, num_high + 1):
                    count += 1
            if count >= rounds_high:
                check = True

        return check

class Group(BaseGroup):
    # Group level data
    immoral_payoff = models.BooleanField(
        choices=[
            [0, 'X'],
            [1, 'Y']
        ]
    )
    group_suggestion = models.BooleanField(
        choices=[
            [0, 'Project X'],
            [1, 'Project Y']
        ]
    )
    total_vote_in_group = models.PositiveIntegerField()
    vote_to_win = models.PositiveIntegerField()
    x_payout = models.PositiveIntegerField()
    y_payout = models.PositiveIntegerField()
    total_vote_x = models.PositiveIntegerField()
    total_vote_y = models.PositiveIntegerField()
    message_space = models.CharField()
    alpha_average = models.FloatField()
    conflict_round = models.BooleanField()
    group_moral_cost = models.BooleanField(
        choices=[
            [0, 'No'],
            [1, 'Yes']
        ]
    )
    g_final_decision = models.BooleanField(
        choices=[[0, 'Project X'],
                 [1, 'Project Y']]
    )

    def assign_ids(self):
        """
        Assign players id in round for each player in the game
        """
        group_id_rounds = literal_eval(Constants.group_id_rounds)
        for i, player in enumerate(self.get_players()):
            player.id_in_round = group_id_rounds['player_{}'.format(i)][self.round_number - 1]

    def assign_payoff_rounds(self):
        """
        Assign players payoff rounds for each player in the game
        """
        group_payoff_rounds = literal_eval(Constants.group_payoff_rounds)
        for i, player in enumerate(self.get_players()):
            player.payoff_rounds = group_payoff_rounds['player_{}'.format(i)][self.round_number - 1]

    def assign_vote_weight(self):
        """
        Assign player vote weight for each player in the game
        """
        treatment_in_round = literal_eval(Constants.round_order)[self.round_number - 1]
        treatment_info = literal_eval(Constants.treatment_dict)['treatment_{}'.format(treatment_in_round)]

        for player in self.get_players():
            if player.id_in_round:
                player.vote_weight = max(treatment_info['votes'])
            else:
                player.vote_weight = 1

    def assign_vote_to_win(self):
        self.vote_to_win = literal_eval(
            Constants.treatment_dict)['treatment_{}'.format(self.round_number - 1)]['quota']

    def assign_moral_cost(self):
        """
        Determine whether players/groups voted in their own interest or in favor of the decision maker
        """

        if self.x_payout > self.y_payout:
            project = 0
            if self.message_space == 'Project X':
                self.group_moral_cost = True
            else:
                self.group_moral_cost = False
        elif self.y_payout > self.x_payout:
            project = 1
            if self.message_space == 'Project Y':
                self.group_moral_cost = True
            else:
                self.group_moral_cost = False
        else:
            self.group_moral_cost = False

        for player in self.get_players():
            player.moral_cost(project)

    def assign_conflict_round(self):
        """
        Determine if there is conflict in a given round or not
        """
        conflict_round = literal_eval(Constants.group_conflict_rounds)[self.round_number - 1]
        self.conflict_round = conflict_round

    def assign_relative_payout(self):
        """
        Assign the relative payout between the two option that are presented
        """

        if self.conflict_round:
            if self.immoral_payoff:
                self.y_payout = 16
                self.x_payout = 4
            else:
                self.y_payout = 4
                self.x_payout = 16
        else:
            payout_list = [4, 16]
            random.shuffle(payout_list)
            self.x_payout = payout_list[0]
            self.y_payout = payout_list[1]

    def total_vote_count(self):
        """
        Count the number of votes that are cast for each option
        """
        total_x_count = 0
        total_y_count = 0
        for player in self.get_players():
            if player.id_in_group != Constants.players_per_group:
                if player.vote:
                    total_y_count += player.vote_weight
                else:
                    total_x_count += player.vote_weight

        self.total_vote_x = total_x_count
        self.total_vote_y = total_y_count
        self.determine_suggestion(total_x_count, total_y_count)

    def determine_suggestion(self, total_x_count, total_y_count):
        """
        Determine the suggestion that the group will send to the decision maker
        """
        if total_x_count > self.vote_to_win:
            self.message_space = "Project X will earn you more money than Project Y"
            self.group_suggestion = False
        elif total_y_count > self.vote_to_win:
            self.message_space = "Project Y will earn you more money than Project X"
            self.group_suggestion = True

    def total_vote_display(self):
        """sum up the total votes in group"""
        count = 0
        for player in self.get_players():
            if player.id_in_round != Constants.players_per_group:
                count += player.vote_weight
        self.total_vote_in_group = count

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
            if player.participant.vars['role'] != 6:
                if player.belief_average < self.alpha_average + .02 and player.belief_average > self.alpha_average - .02:
                    player.belief_payout = 18
                elif player.belief_average < self.alpha_average + 1 and player.belief_average > self.alpha_average - 1:
                    player.belief_payout = 6
                else:
                    player.belief_payout = 0



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
                [0, 'No'],
                [1, 'Yes']
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
    belief_average = models.DecimalField(min=0, max=30,max_digits=3,decimal_places=1)

    final_decision = models.BooleanField(
        choices=[
            [0, 'Project X'],
            [1, 'Project Y']
        ]
    )

    field = models.CharField()
    age = models.IntegerField(min=18, max=100)
    gender = models.CharField(
        choices=['Male', 'Female'],
        widget=widgets.RadioSelect(),
    )

    def moral_cost(self, project):
        """
        Determine if the player voted in their own interest or in the interest of the decision maker
        """

        if project == 0:
            if self.vote:
                self.individual_moral_cost = False
            else:
                self.individual_moral_cost = True
        elif project == 1:
            if self.vote:
                self.individual_moral_cost = True
            else:
                self.individual_moral_cost = False
        else:
            self.individual_moral_cost = False




