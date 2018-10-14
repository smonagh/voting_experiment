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
    conversion_rate = 6
    treatments = 3


class Subsession(BaseSubsession):
    treatment_dict = models.LongStringField(initial='{}')
    players_id = models.LongStringField(initial='{}')
    round_order = models.LongStringField(initial='[]')
    group_id_rounds = models.LongStringField(initial='{}')
    group_payoff_rounds = models.LongStringField(initial='{}')
    group_conflict_rounds = models.LongStringField(initial='[]')
    tracker_dict = models.LongStringField(initial='{}')
    followed_average = models.IntegerField()

    def creating_session(self):
        """Assign variables before experiment starts"""

        self.randomize_players()
        self.establish_parameters()

    def randomize_players(self):
        """
        Randomize the players for each round
        """
        # If round == 1 then set payoffs
        if self.round_number == 1:
            self.gen_payment_rounds()

        self.group_payoff_rounds = self.in_round(1).group_payoff_rounds
        self.assign_player_payoff_rounds()
        players_dict = {'player_{}'.format(i): [] for i in range(1, Constants.players_per_group + 1)}
        if self.round_number <= Constants.num_rounds:
            players = self.get_players()
            random.shuffle(players)
            for player in players:
                players_dict['player_{}'.format(player.participant.vars['id'])].append(player)

        group_matrix = []
        while players_dict['player_1']:
            new_group = [players_dict['player_{}'.format(i)].pop() for i in range(1, Constants.players_per_group + 1)]
            group_matrix.append(new_group)

        self.players_id = str(players_dict)
        self.set_group_matrix(group_matrix)

    def establish_parameters(self):

        # Establish group and player parameters if not the last round
        if self.round_number < Constants.num_rounds:
            self.parameters_for_game()
            self.group_parameters()

    def parameters_for_game(self):
        if self.round_number == 1:
            self.set_treatments()
            self.gen_payment_rounds()
            self.gen_round_order()
            self.gen_tracker_dict()
            self.set_conflict_rounds()
            self.set_id_rounds()
        else:
            self.treatment_dict = self.in_round(1).treatment_dict
            self.players_id = self.in_round(1).players_id
            self.round_order = self.in_round(1).round_order
            self.group_id_rounds = self.in_round(1).group_id_rounds
            self.group_payoff_rounds = self.in_round(1).group_payoff_rounds
            self.group_conflict_rounds = self.in_round(1).group_conflict_rounds
            self.tracker_dict = self.in_round(1).tracker_dict

    def group_parameters(self):
        for group in self.get_groups():
            group.assign_ids()
            group.assign_vote_weight()
            group.assign_conflict_round()
            group.assign_vote_to_win()
            group.immoral_payoff = random.randint(0, 1)
            group.assign_relative_payout()


    def set_treatments(self):
        """
        Define treatments for the game.
        """

        treatment_dict = literal_eval(self.treatment_dict)
        for i in range(1, Constants.treatments + 1):
            if i == 1:
                treatment_dict['treatment_1'] = {'votes': [2, 2, 1, 1, 1], 'quota': 4,
                                                 'high': 4,  'conflict': 7, 'num_high': 2}
            elif i == 2:
                treatment_dict['treatment_2'] = {'votes': [3, 1, 1, 1, 1], 'quota': 4,
                                                 'high': 2, 'conflict': 10, 'num_high': 1}
            elif i == 3:
                treatment_dict['treatment_3'] = {'votes': [1, 1, 1, 1, 1], 'quota': 3,
                                                 'high': 10, 'conflict': 5, 'num_high': 5}

        self.treatment_dict = str(treatment_dict)

    def gen_round_order(self):
        """
        Function generates the rounds that each group will play with
        in the game
        """

        round_order = [i for i in range(1, Constants.treatments + 1)] * int(
            ((Constants.num_rounds - 1)/Constants.treatments))
        random.shuffle(round_order)

        self.round_order = str(round_order)


    def gen_payment_rounds(self):
        """
        Generates the rounds in which payers are paid on for each player
        """
        payoff_dict = literal_eval(self.group_payoff_rounds)

        for index, player in enumerate(self.get_players()):
            if player.id_in_group == Constants.players_per_group:
                payoff_dict['player_{}'.format(player.id_in_group)] = [i for i in range(1, Constants.num_rounds)]
            else:
                payoff_list = []
                while len(payoff_list) != 6:
                    rand_num = random.randint(1, 31)
                    if rand_num not in payoff_list:
                        payoff_list.append(rand_num)

                payoff_dict['player_{}'.format(player.id_in_group)] = payoff_list

        self.group_payoff_rounds = str(payoff_dict)

    def assign_player_payoff_rounds(self):
        """
        If round number is equal to the to the number contained in the payoff dictionary
        set the players payoff for the round to true.
        """
        payoff_dict = literal_eval(self.group_payoff_rounds)

        for player in self.get_players():
            payoff_list = payoff_dict['player_{}'.format(player.id_in_group)]
            if self.round_number in payoff_list:
                player.payoff_rounds = True
            else:
                player.payoff_rounds = False

    def gen_tracker_dict(self):
        """
        Generate a dictionary that is used to track player assignment to rounds
        """

        tracker_dict = literal_eval(self.tracker_dict)
        for player in range(1, Constants.players_per_group + 1):
            tracker_dict['player_{}'.format(player)] = {}

        for value in tracker_dict.values():
            for treatment in range(1, Constants.treatments + 1):
                value['treatment_{}'.format(treatment)] = {}
                value['treatment_{}'.format(treatment)]['id'] = [0] * (Constants.num_rounds - 1)
                value['treatment_{}'.format(treatment)]['payoff'] = [0] * (Constants.num_rounds - 1)

        self.tracker_dict = str(tracker_dict)

    def set_conflict_rounds(self):
        """
        Determine which rounds there is a competing payoff and in which rounds there is an equal payoff
        """
        round_order = literal_eval(self.round_order)
        treatment_dict = literal_eval(self.treatment_dict)
        conflict_rounds = []
        conflict_tracker = {'treatment_{}'.format(i): 0 for i in range(1, Constants.treatments + 1)}

        for index, cur_round in enumerate(round_order):
            index += 1

            if conflict_tracker['treatment_{}'.format(cur_round)] >= treatment_dict['treatment_{}'.format(
                    cur_round)]['conflict']:
                conflict_rounds.append(False)
            else:
                rounds_needed = treatment_dict['treatment_{}'.format(
                    cur_round)]['conflict'] - conflict_tracker['treatment_{}'.format(cur_round)]
                result = self.check_lower_bound(cur_round, treatment_dict, index, rounds_needed)
                conflict_rounds.append(result)
                conflict_tracker['treatment_{}'.format(cur_round)] += result
        print(conflict_tracker)
        self.group_conflict_rounds = str(conflict_rounds)

    def check_lower_bound(self, cur_round, treatment_dict, cur_round_number, rounds_needed):
        """
        Make sure that result is assigned true if there are too few rounds left in the game to
        assign a true statement
        """

        remainder = (Constants.num_rounds - 1) - cur_round_number
        #print('***************: ', va, remainder, var - remainder)
        if rounds_needed - remainder <= 0:
            result = True
        else:
            result = np.random.choice([False, True])

        return result

    def set_id_rounds(self):
        """
        Define each players id in the group for each round in the game
        """
        tracker_dict = literal_eval(self.tracker_dict)
        round_order = literal_eval(self.round_order)
        conflict_check = literal_eval(self.group_conflict_rounds)
        treatment_dict = literal_eval(self.treatment_dict)
        conflict_dict = {'player_{}'.format(i):{
            'treatment_1': 0, 'treatment_2': 0} for i in range(1, Constants.players_per_group)}

        for i, current_round in enumerate(round_order):
            check = True
            second_check = True
            while check:
                sample_list = [i for i in range(1, Constants.players_per_group)]
                sample = np.random.choice(sample_list, 5, replace=False)
                player_list = []
                treatment_list = []
                for player_num in range(1, Constants.players_per_group):
                    tracker_dict['player_{}'.format(player_num)]['treatment_{}'.format(
                        current_round)]['id'][i] = sample[player_num - 1]

                    if current_round in [1, 2]:
                        if current_round == 1 and sample[player_num - 1] in [1, 2] and conflict_check[i]:
                            if conflict_dict['player_{}'.format(player_num)][
                                  'treatment_1'] >= treatment_dict['treatment_1']['high']/2:
                                second_check = True
                                break
                            else:
                                conflict_dict['player_{}'.format(player_num)][
                                    'treatment_1'] += 1
                                second_check = False
                                player_list.append(player_num)
                                treatment_list.append(1)

                        elif current_round == 2 and sample[player_num - 1] == 1 and conflict_check[i]:
                            if conflict_dict['player_{}'.format(player_num)][
                                  'treatment_2'] >= treatment_dict['treatment_2']['high']/2:
                                second_check = True
                                break
                            else:
                                conflict_dict['player_{}'.format(player_num)][
                                    'treatment_2'] += 1
                                second_check = False
                                player_list.append(player_num)
                                treatment_list.append(2)
                        else:
                            second_check = False
                    else:
                        second_check = False

                if not second_check:
                    check, tracker_dict = self.check_max_id_condition(current_round, tracker_dict)
                    print(check)
                    if check and player_list:
                        print(player_list, treatment_list)
                        print('minus hit')
                        for treatment, player in enumerate(player_list):
                            conflict_dict['player_{}'.format(player)][
                                'treatment_{}'.format(treatment_list[treatment])] -= 1

        self.tracker_dict = str(tracker_dict)
        self.set_group_id(tracker_dict)
        print('we did it')

    def set_group_id(self, tracker_dict):
        """
        Consolidate the three indices into one by ignoring zero values contained in the tracker dict
        """
        group_id_rounds = literal_eval(self.group_id_rounds)
        for player in range(1, Constants.players_per_group):
            player_list = []
            for cur_round in range(Constants.num_rounds - 1):
                for treatment in range(1, Constants.treatments + 1):
                    if tracker_dict['player_{}'.format(player)]['treatment_{}'.format(treatment)]['id'][cur_round] > 0:
                        player_list.append(tracker_dict['player_{}'.format(player)][
                                               'treatment_{}'.format(treatment)]['id'][cur_round])
            group_id_rounds['player_{}'.format(player)] = player_list

        group_id_rounds['player_6'] = [6] * Constants.num_rounds

        self.group_id_rounds = str(group_id_rounds)

    def check_max_id_condition(self, current_round, tracker_dict):
        """
        Check to make sure that players have not been assigned to the max position in round list more than the times
        that they are allowed to occupy that position.
        """
        treatment_dict = literal_eval(self.treatment_dict)
        num_high = treatment_dict['treatment_{}'.format(current_round)]['num_high']
        high = treatment_dict['treatment_{}'.format(current_round)]['high']

        check = False
        for player_num in range(1, Constants.players_per_group):
            count_list = tracker_dict['player_{}'.format(player_num)]['treatment_{}'.format(current_round)]['id']

            count = 0
            for player_id in count_list:
                if player_id in range(1, num_high + 1):
                    count += 1
            if count > high:
                check = True

        return check, tracker_dict

    def final_payoff_return(self):
        group_payoff_rounds = literal_eval(self.group_payoff_rounds)
        for player in self.get_players():
            final_payoff = 0
            for prev in player.in_previous_rounds():
                if prev.payout and prev.round_number in group_payoff_rounds['player_{}'.format(player.id_in_group)]:
                    final_payoff += prev.payout

            if player.id_in_group < Constants.players_per_group:
                player.final_payout = final_payoff + player.in_round(30).belief_payout
            player.final_us_payout = final_payoff/Constants.conversion_rate

    def set_followed_average(self):

        decision_list = self.get_decision_makers()
        average_list = []
        for player in decision_list:
            followed_sum = 0
            for prev_play in player.in_all_rounds():
                if prev_play.followed:
                    followed_sum += 1

            average_list.append(followed_sum/(Constants.num_rounds - 1))

        self.followed_average = sum(average_list)/len(decision_list)
        return self.followed_average

    def get_decision_makers(self):
        """Return a list containing the decision makers in the subsession"""

        decision_maker_list = []
        for player in self.get_players():
            if player.id_in_group == Constants.players_per_group:
                decision_maker_list.append(player)

        return decision_maker_list

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
        group_id_rounds = literal_eval(self.subsession.group_id_rounds)
        if self.round_number != Constants.num_rounds:
            for player in self.get_players():
                player.id_in_round = group_id_rounds['player_{}'.format(player.id_in_group)][self.round_number - 1]

    def assign_payoff_rounds(self):
        """
        Assign players payoff rounds for each player in the game
        """
        group_payoff_rounds = literal_eval(self.subsession.group_payoff_rounds)
        for i, player in enumerate(self.get_players()):
            player.payoff_rounds = group_payoff_rounds['player_{}'.format(i)][self.round_number - 1]

    def assign_vote_weight(self):
        """
        Assign player vote weight for each player in the game
        """
        treatment_in_round = literal_eval(self.subsession.round_order)[self.round_number - 1]
        treatment_info = literal_eval(self.subsession.treatment_dict)['treatment_{}'.format(treatment_in_round)]

        for player in self.get_players():
            if player.id_in_round <= treatment_info['num_high']:
                player.vote_weight = max(treatment_info['votes'])
            else:
                player.vote_weight = 1

    def assign_vote_to_win(self):
        round_order = literal_eval(self.subsession.round_order)
        cur_round = round_order[self.round_number - 1]
        self.vote_to_win = literal_eval(
            self.subsession.treatment_dict)['treatment_{}'.format(cur_round)]['quota']

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
        conflict_round = literal_eval(self.subsession.group_conflict_rounds)[self.round_number - 1]
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
        if total_x_count >= self.vote_to_win:
            self.message_space = "Project X will earn you more money than Project Y"
            self.group_suggestion = False
        elif total_y_count >= self.vote_to_win:
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
                if player.id_in_group < Constants.players_per_group:
                    player.payout = self.x_payout
                else:
                    player.payout = self.y_payout
            elif self.g_final_decision == 1:
                if player.id_in_group < Constants.players_per_group:
                    player.payout = self.y_payout
                else:
                    player.payout = self.x_payout

    def set_add_payoffs(self, average):
        """Add players payoff from bonus question"""
        for player in self.get_players():
            if player.id_in_group != Constants.players_per_group:
                if player.belief_average:
                    print(player.belief_average)
                    if average - .02 <= float(player.belief_average) <= average + .02:
                        player.belief_payout = 18
                    elif average - 1 <= float(player.belief_average) <= average + 1:
                        player.belief_payout = 6
                    else:
                        player.belief_payout = 0

    def set_final_decision(self):
        """Determine the final decision for group from the decision maker"""
        player = self.get_player_by_id(Constants.players_per_group)
        self.g_final_decision = player.final_decision

    def determine_followed(self):
        """Determine if the decision maker followed the group suggestion for the round"""
        player = self.get_player_by_id(Constants.players_per_group)

        if self.group_suggestion == 0:
            if player.final_decision == 0:
                player.followed = True
            else:
                player.followed = False

        elif self.group_suggestion == 1:
            if player.final_decision == 1:
                player.followed = True
            else:
                player.followed = False

class Player(BasePlayer):
    # Player level data
    vote_weight = models.PositiveIntegerField()
    id_in_round = models.PositiveIntegerField()
    payout = models.PositiveIntegerField()
    payoff_rounds = models.BooleanField()
    final_payout = models.PositiveIntegerField()
    final_us_payout = models.PositiveIntegerField()
    belief_payout = models.PositiveIntegerField()
    followed = models.BooleanField()
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
    belief_average = models.DecimalField(min=0, max=30, max_digits=3, decimal_places=1)

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




