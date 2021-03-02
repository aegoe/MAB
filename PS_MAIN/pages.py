from otree.api import (
    Currency as c, currency_range, BasePlayer
)

from _builtin import Page, WaitPage
from .models import Constants
import random
from numpy.random import choice
import numpy
import time
#from numpy import random
#from otree_mturk_utils.views import Page, CustomMturkWaitPage
from functools import reduce
from collections import Counter
import string


########################################################################################################################
# DECISION #############################################################################################################
########################################################################################################################

class DecisionTransition(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.player.round_number == 1

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'end_button': self.player.end_button,
               'payoff': self.participant.payoff,
               'sampling_round': self.participant.vars['sampling_round'],
               'points_sampling': self.participant.vars['points_sampling'],
               'round_number': self.player.round_number,
               }


##lower mean risky option
class PriorsA(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == self.participant.vars['options']['A']

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'draw': self.participant.vars['draw'],
               'sampling': self.participant.vars['sampling'],

               }

class DecisionA1(Page):
    form_model = 'player'

    def is_displayed(self):
        if not self.participant.vars['sampling'] and not self.participant.vars['choice'] and self.player.decision_a_page == 1:
            return self.round_number == self.participant.vars['options']['A']
        elif not self.participant.vars['sampling'] and self.participant.vars['choice'] and self.player.decision_a_page <= 3:
            return self.round_number == self.participant.vars['options']['A']


    def get_form_fields(self):
        if self.participant.vars['choice'] and not self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3']

        elif self.participant.vars['choice'] and self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3', 'option_safe']

        elif not self.participant.vars['choice'] and not self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3']

        elif not self.participant.vars['choice'] and self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3', 'option_safe']

    def error_message(self, values):
        if self.participant.vars['choice'] and not self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] < 1:
                return 'You have to use your point to choose an urn.'
            elif values['option_1'] + values['option_2'] + values['option_3'] > 1:
                return 'You can only choose one option per round.'

        elif self.participant.vars['choice'] and self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] < 1:
                return 'You have to use your point to choose an urn.'
            elif values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] > 1:
                return 'You can only choose one option per round.'

        elif not self.participant.vars['choice'] and not self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] < 3:
                return 'You have to use all three points'
            elif values['option_1'] + values['option_2'] + values['option_3'] > 3:
                return 'You can only use three points per round'

        elif not self.participant.vars['choice'] and self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] < 3:
                return 'You have to use all three points'
            elif values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] > 3:
                return 'You can only use three points per round'

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'safe_option': Constants.safe_option,
               'endowment_choice': Constants.endowment_choice,
               'endowment_points': Constants.endowment_points,
               'safe': self.participant.vars['safe'],
               'draw': self.participant.vars['draw'],
               'sampling': self.participant.vars['sampling'],
               'payoff': self.participant.payoff,
               }

    def before_next_page(self):

        if self.participant.vars['choice']:

            Urn_1 = ['0', '1', '2', '3', '4', '5', '6', '7']
            Urn_2 = ['-9', '-5', '-4', '-3', '35', '40', '50', '60']
            Urn_3 = ['3']

            weights_1 = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
            weights_2 = [0.2, 0.2, 0.2, 0.2, 0.05, 0.05, 0.05, 0.05]
            weights_3 = [1]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str


            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)

            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3

            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '0':
                        data_counts[i][k] = v * 0
                    elif k == '1':
                        data_counts[i][k] = v * 1
                    elif k == '2':
                        data_counts[i][k] = v * 2
                    elif k == '3':
                        data_counts[i][k] = v * 3
                    elif k == '4':
                        data_counts[i][k] = v * 4
                    elif k == '5':
                        data_counts[i][k] = v * 5
                    elif k == '6':
                        data_counts[i][k] = v * 6
                    elif k == '7':
                        data_counts[i][k] = v * 7
                    elif k == '8':
                        data_counts[i][k] = v * 8
                    elif k == '9':
                        data_counts[i][k] = v * 9
                    elif k == '10':
                        data_counts[i][k] = v * 10
                    elif k == '20':
                        data_counts[i][k] = v * 20
                    elif k == '25':
                        data_counts[i][k] = v * 25
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40

            self.player.payoff = 0
            payoffs = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    payoffs += values

            self.player.payoff = payoffs

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0

            payoffs_1 = 0
            payoffs_2 = 0
            payoffs_3 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        payoffs_1 += v
                    if i == 'count_2':
                        payoffs_2 += v
                    if i == 'count_3':
                        payoffs_3 += v

            self.player.payoff_1 = payoffs_1
            self.player.payoff_2 = payoffs_2
            self.player.payoff_3 = payoffs_3

            if (self.round_number - self.participant.vars['sampling_round']) % 2 == 0 and self.round_number >2:
                self.player.payoff_1_m2 = self.player.in_round(self.round_number - 2).payoff_1
                self.player.payoff_2_m2 = self.player.in_round(self.round_number - 2).payoff_2
                self.player.payoff_3_m2 = self.player.in_round(self.round_number - 2).payoff_3

                self.player.payoff_1_m1 = self.player.in_round(self.round_number - 1).payoff_1
                self.player.payoff_2_m1 = self.player.in_round(self.round_number - 1).payoff_2
                self.player.payoff_3_m1 = self.player.in_round(self.round_number - 1).payoff_3

                self.player.payoff_all3 = self.player.payoff + self.player.in_round(self.round_number - 2).payoff + self.player.in_round(self.round_number - 1).payoff

                self.player.payoff_1_all3 = self.player.payoff_1 + self.player.in_round(self.round_number - 2).payoff_1 + self.player.in_round(self.round_number - 1).payoff_1
                self.player.payoff_2_all3 = self.player.payoff_2 + self.player.in_round(self.round_number - 2).payoff_2 + self.player.in_round(self.round_number - 1).payoff_2
                self.player.payoff_3_all3 = self.player.payoff_3 + self.player.in_round(self.round_number - 2).payoff_3 + self.player.in_round(self.round_number - 1).payoff_3

                self.player.urn_draws_1_m2 = self.player.in_round(self.round_number - 2).urn_draws_1
                self.player.urn_draws_2_m2 = self.player.in_round(self.round_number - 2).urn_draws_2
                self.player.urn_draws_3_m2 = self.player.in_round(self.round_number - 2).urn_draws_3

                self.player.urn_draws_1_m1 = self.player.in_round(self.round_number - 1).urn_draws_1
                self.player.urn_draws_2_m1 = self.player.in_round(self.round_number - 1).urn_draws_2
                self.player.urn_draws_3_m1 = self.player.in_round(self.round_number - 1).urn_draws_3

                self.player.option_1_all3 = self.player.option_1 + self.player.in_round(self.round_number - 2).option_1 + self.player.in_round(self.round_number - 1).option_1
                self.player.option_2_all3 = self.player.option_2 + self.player.in_round(self.round_number - 2).option_2 + self.player.in_round(self.round_number - 1).option_2
                self.player.option_3_all3 = self.player.option_3 + self.player.in_round(self.round_number - 2).option_3 + self.player.in_round(self.round_number - 1).option_3

            else:
                pass

        elif not self.participant.vars['choice'] :

            Urn_1 = ['0', '1', '2', '3', '4', '5', '6', '7']
            Urn_2 = ['-9', '-5', '-4', '-3', '35', '40', '50', '60']
            Urn_3 = ['3']

            weights_1 = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
            weights_2 = [0.2, 0.2, 0.2, 0.2, 0.05, 0.05, 0.05, 0.05]
            weights_3 = [1]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str

            print(self.player.urn_draws_1)
            print(draws_1)
            print(draws_2)
            print(draws_3)

            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)

            print(count_1)
            print(count_2)
            print(count_3)



            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3


            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '0':
                        data_counts[i][k] = v * 0
                    elif k == '1':
                        data_counts[i][k] = v * 1
                    elif k == '2':
                        data_counts[i][k] = v * 2
                    elif k == '3':
                        data_counts[i][k] = v * 3
                    elif k == '4':
                        data_counts[i][k] = v * 4
                    elif k == '5':
                        data_counts[i][k] = v * 5
                    elif k == '6':
                        data_counts[i][k] = v * 6
                    elif k == '7':
                        data_counts[i][k] = v * 7
                    elif k == '8':
                        data_counts[i][k] = v * 8
                    elif k == '9':
                        data_counts[i][k] = v * 9
                    elif k == '10':
                        data_counts[i][k] = v * 10
                    elif k == '20':
                        data_counts[i][k] = v * 20
                    elif k == '25':
                        data_counts[i][k] = v * 25
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40

            self.player.payoff = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    self.player.payoff += values

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        self.player.payoff_1 += v
                    if i == 'count_2':
                        self.player.payoff_2 += v
                    if i == 'count_3':
                        self.player.payoff_3 += v

        self.player.decision_a_page += 1


##higher mean risky option
class PriorsB(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == self.participant.vars['options']['B']

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'draw': self.participant.vars['draw'],
               'sampling': self.participant.vars['sampling'],

               }

class DecisionB1(Page):
    form_model = 'player'

    def is_displayed(self):
        if not self.participant.vars['sampling'] and not self.participant.vars['choice'] and self.player.decision_b_page == 1:
            return self.round_number == self.participant.vars['options']['B']
        elif not self.participant.vars['sampling'] and self.participant.vars['choice'] and self.player.decision_b_page <= 3:
            return self.round_number == self.participant.vars['options']['B']


    def get_form_fields(self):
        if self.participant.vars['choice'] and not self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3']

        elif self.participant.vars['choice'] and self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3', 'option_safe']

        elif not self.participant.vars['choice'] and not self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3']

        elif not self.participant.vars['choice'] and self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3', 'option_safe']

    def error_message(self, values):
        if self.participant.vars['choice'] and not self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] < 1:
                return 'You have to use your point to choose an urn.'
            elif values['option_1'] + values['option_2'] + values['option_3'] > 1:
                return 'You can only choose one option per round.'

        elif self.participant.vars['choice'] and self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] < 1:
                return 'You have to use your point to choose an urn.'
            elif values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] > 1:
                return 'You can only choose one option per round.'

        elif not self.participant.vars['choice'] and not self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] < 3:
                return 'You have to use all three points'
            elif values['option_1'] + values['option_2'] + values['option_3'] > 3:
                return 'You can only use three points per round'

        elif not self.participant.vars['choice'] and self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] < 3:
                return 'You have to use all three points'
            elif values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] > 3:
                return 'You can only use three points per round'

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'safe_option': Constants.safe_option,
               'endowment_choice': Constants.endowment_choice,
               'endowment_points': Constants.endowment_points,
               'safe': self.participant.vars['safe'],
               'draw': self.participant.vars['draw'],
               'sampling': self.participant.vars['sampling'],
               'payoff': self.participant.payoff,

               }

    def before_next_page(self):

        if self.participant.vars['choice'] and not self.participant.vars['safe'] :

            Urn_1 = ['0', '1', '2', '3', '4', '5', '6', '7']
            Urn_2 = ['-9', '-5', '-4', '-3', '35', '40', '50', '60']
            Urn_3 = ['3']

            weights_1 = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
            weights_2 = [0.2, 0.2, 0.2, 0.2, 0.05, 0.05, 0.05, 0.05]
            weights_3 = [1]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str


            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)

            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3

            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '0':
                        data_counts[i][k] = v * 0
                    elif k == '1':
                        data_counts[i][k] = v * 1
                    elif k == '2':
                        data_counts[i][k] = v * 2
                    elif k == '3':
                        data_counts[i][k] = v * 3
                    elif k == '4':
                        data_counts[i][k] = v * 4
                    elif k == '5':
                        data_counts[i][k] = v * 5
                    elif k == '6':
                        data_counts[i][k] = v * 6
                    elif k == '7':
                        data_counts[i][k] = v * 7
                    elif k == '8':
                        data_counts[i][k] = v * 8
                    elif k == '9':
                        data_counts[i][k] = v * 9
                    elif k == '10':
                        data_counts[i][k] = v * 10
                    elif k == '20':
                        data_counts[i][k] = v * 20
                    elif k == '25':
                        data_counts[i][k] = v * 25
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40

            self.player.payoff = 0
            payoffs = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    payoffs += values

            self.player.payoff = payoffs

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0

            payoffs_1 = 0
            payoffs_2 = 0
            payoffs_3 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        payoffs_1 += v
                    if i == 'count_2':
                        payoffs_2 += v
                    if i == 'count_3':
                        payoffs_3 += v

            self.player.payoff_1 = payoffs_1
            self.player.payoff_2 = payoffs_2
            self.player.payoff_3 = payoffs_3

            if (self.round_number - self.participant.vars['sampling_round']) % 2 == 0 and self.round_number >2:
                self.player.payoff_1_m2 = self.player.in_round(self.round_number - 2).payoff_1
                self.player.payoff_2_m2 = self.player.in_round(self.round_number - 2).payoff_2
                self.player.payoff_3_m2 = self.player.in_round(self.round_number - 2).payoff_3

                self.player.payoff_1_m1 = self.player.in_round(self.round_number - 1).payoff_1
                self.player.payoff_2_m1 = self.player.in_round(self.round_number - 1).payoff_2
                self.player.payoff_3_m1 = self.player.in_round(self.round_number - 1).payoff_3

                self.player.payoff_all3 = self.player.payoff + self.player.in_round(self.round_number - 2).payoff + self.player.in_round(self.round_number - 1).payoff

                self.player.payoff_1_all3 = self.player.payoff_1 + self.player.in_round(self.round_number - 2).payoff_1 + self.player.in_round(self.round_number - 1).payoff_1
                self.player.payoff_2_all3 = self.player.payoff_2 + self.player.in_round(self.round_number - 2).payoff_2 + self.player.in_round(self.round_number - 1).payoff_2
                self.player.payoff_3_all3 = self.player.payoff_3 + self.player.in_round(self.round_number - 2).payoff_3 + self.player.in_round(self.round_number - 1).payoff_3

                self.player.urn_draws_1_m2 = self.player.in_round(self.round_number - 2).urn_draws_1
                self.player.urn_draws_2_m2 = self.player.in_round(self.round_number - 2).urn_draws_2
                self.player.urn_draws_3_m2 = self.player.in_round(self.round_number - 2).urn_draws_3

                self.player.urn_draws_1_m1 = self.player.in_round(self.round_number - 1).urn_draws_1
                self.player.urn_draws_2_m1 = self.player.in_round(self.round_number - 1).urn_draws_2
                self.player.urn_draws_3_m1 = self.player.in_round(self.round_number - 1).urn_draws_3

                self.player.option_1_all3 = self.player.option_1 + self.player.in_round(self.round_number - 2).option_1 + self.player.in_round(self.round_number - 1).option_1
                self.player.option_2_all3 = self.player.option_2 + self.player.in_round(self.round_number - 2).option_2 + self.player.in_round(self.round_number - 1).option_2
                self.player.option_3_all3 = self.player.option_3 + self.player.in_round(self.round_number - 2).option_3 + self.player.in_round(self.round_number - 1).option_3

            else:
                pass

        elif not self.participant.vars['choice'] and not self.participant.vars['safe']:

            Urn_1 = ['0', '1', '2', '3', '4', '5', '6', '7']
            Urn_2 = ['-9', '-5', '-4', '-3', '35', '40', '50', '60']
            Urn_3 = ['3']

            weights_1 = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
            weights_2 = [0.2, 0.2, 0.2, 0.2, 0.05, 0.05, 0.05, 0.05]
            weights_3 = [1]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str

            print(self.player.urn_draws_1)
            print(draws_1)
            print(draws_2)
            print(draws_3)

            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)

            print(count_1)
            print(count_2)
            print(count_3)



            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3


            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '0':
                        data_counts[i][k] = v * 0
                    elif k == '1':
                        data_counts[i][k] = v * 1
                    elif k == '2':
                        data_counts[i][k] = v * 2
                    elif k == '3':
                        data_counts[i][k] = v * 3
                    elif k == '4':
                        data_counts[i][k] = v * 4
                    elif k == '5':
                        data_counts[i][k] = v * 5
                    elif k == '6':
                        data_counts[i][k] = v * 6
                    elif k == '7':
                        data_counts[i][k] = v * 7
                    elif k == '8':
                        data_counts[i][k] = v * 8
                    elif k == '9':
                        data_counts[i][k] = v * 9
                    elif k == '10':
                        data_counts[i][k] = v * 10
                    elif k == '20':
                        data_counts[i][k] = v * 20
                    elif k == '25':
                        data_counts[i][k] = v * 25
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40

            self.player.payoff = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    self.player.payoff += values

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        self.player.payoff_1 += v
                    if i == 'count_2':
                        self.player.payoff_2 += v
                    if i == 'count_3':
                        self.player.payoff_3 += v

        self.player.decision_b_page += 1


##same urns as A nd B, but Bernoulli instead of safe
class PriorsC(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == self.participant.vars['options']['C']

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'draw': self.participant.vars['draw'],
               'sampling': self.participant.vars['sampling'],

               }

class DecisionC1(Page):
    form_model = 'player'

    def is_displayed(self):
        if not self.participant.vars['sampling'] and not self.participant.vars['choice'] and self.player.decision_c_page == 1:
            return self.round_number == self.participant.vars['options']['C']
        elif not self.participant.vars['sampling'] and self.participant.vars['choice'] and self.player.decision_c_page <= 3:
            return self.round_number == self.participant.vars['options']['C']


    def get_form_fields(self):
        if self.participant.vars['choice'] and not self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3']

        elif self.participant.vars['choice'] and self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3', 'option_safe']

        elif not self.participant.vars['choice'] and not self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3']

        elif not self.participant.vars['choice'] and self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3', 'option_safe']

    def error_message(self, values):
        if self.participant.vars['choice'] and not self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] < 1:
                return 'You have to use your point to choose an urn.'
            elif values['option_1'] + values['option_2'] + values['option_3'] > 1:
                return 'You can only choose one option per round.'

        elif self.participant.vars['choice'] and self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] < 1:
                return 'You have to use your point to choose an urn.'
            elif values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] > 1:
                return 'You can only choose one option per round.'

        elif not self.participant.vars['choice'] and not self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] < 3:
                return 'You have to use all three points'
            elif values['option_1'] + values['option_2'] + values['option_3'] > 3:
                return 'You can only use three points per round'

        elif not self.participant.vars['choice'] and self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] < 3:
                return 'You have to use all three points'
            elif values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] > 3:
                return 'You can only use three points per round'

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'safe_option': Constants.safe_option,
               'endowment_choice': Constants.endowment_choice,
               'endowment_points': Constants.endowment_points,
               'safe': self.participant.vars['safe'],
               'draw': self.participant.vars['draw'],
               'sampling': self.participant.vars['sampling'],
               'payoff': self.participant.payoff,
               }

    def before_next_page(self):

        if self.participant.vars['choice'] and not self.participant.vars['safe'] and not self.participant.vars['variance']:

            Urn_1 = ['0', '1', '2', '3', '4', '5', '6', '7']
            Urn_2 = ['-9', '-5', '-4', '-3', '35', '40', '50', '60']
            Urn_3 = ['2', '4']

            weights_1 = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
            weights_2 = [0.2, 0.2, 0.2, 0.2, 0.05, 0.05, 0.05, 0.05]
            weights_3 = [0.5, 0.5]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str


            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)

            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3

            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '0':
                        data_counts[i][k] = v * 0
                    elif k == '1':
                        data_counts[i][k] = v * 1
                    elif k == '2':
                        data_counts[i][k] = v * 2
                    elif k == '3':
                        data_counts[i][k] = v * 3
                    elif k == '4':
                        data_counts[i][k] = v * 4
                    elif k == '5':
                        data_counts[i][k] = v * 5
                    elif k == '6':
                        data_counts[i][k] = v * 6
                    elif k == '7':
                        data_counts[i][k] = v * 7
                    elif k == '8':
                        data_counts[i][k] = v * 8
                    elif k == '9':
                        data_counts[i][k] = v * 9
                    elif k == '10':
                        data_counts[i][k] = v * 10
                    elif k == '20':
                        data_counts[i][k] = v * 20
                    elif k == '25':
                        data_counts[i][k] = v * 25
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40

            self.player.payoff = 0
            payoffs = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    payoffs += values

            self.player.payoff = payoffs

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0

            payoffs_1 = 0
            payoffs_2 = 0
            payoffs_3 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        payoffs_1 += v
                    if i == 'count_2':
                        payoffs_2 += v
                    if i == 'count_3':
                        payoffs_3 += v

            self.player.payoff_1 = payoffs_1
            self.player.payoff_2 = payoffs_2
            self.player.payoff_3 = payoffs_3

            if (self.round_number - self.participant.vars['sampling_round']) % 2 == 0 and self.round_number >2:
                self.player.payoff_1_m2 = self.player.in_round(self.round_number - 2).payoff_1
                self.player.payoff_2_m2 = self.player.in_round(self.round_number - 2).payoff_2
                self.player.payoff_3_m2 = self.player.in_round(self.round_number - 2).payoff_3

                self.player.payoff_1_m1 = self.player.in_round(self.round_number - 1).payoff_1
                self.player.payoff_2_m1 = self.player.in_round(self.round_number - 1).payoff_2
                self.player.payoff_3_m1 = self.player.in_round(self.round_number - 1).payoff_3

                self.player.payoff_all3 = self.player.payoff + self.player.in_round(self.round_number - 2).payoff + self.player.in_round(self.round_number - 1).payoff

                self.player.payoff_1_all3 = self.player.payoff_1 + self.player.in_round(self.round_number - 2).payoff_1 + self.player.in_round(self.round_number - 1).payoff_1
                self.player.payoff_2_all3 = self.player.payoff_2 + self.player.in_round(self.round_number - 2).payoff_2 + self.player.in_round(self.round_number - 1).payoff_2
                self.player.payoff_3_all3 = self.player.payoff_3 + self.player.in_round(self.round_number - 2).payoff_3 + self.player.in_round(self.round_number - 1).payoff_3

                self.player.urn_draws_1_m2 = self.player.in_round(self.round_number - 2).urn_draws_1
                self.player.urn_draws_2_m2 = self.player.in_round(self.round_number - 2).urn_draws_2
                self.player.urn_draws_3_m2 = self.player.in_round(self.round_number - 2).urn_draws_3

                self.player.urn_draws_1_m1 = self.player.in_round(self.round_number - 1).urn_draws_1
                self.player.urn_draws_2_m1 = self.player.in_round(self.round_number - 1).urn_draws_2
                self.player.urn_draws_3_m1 = self.player.in_round(self.round_number - 1).urn_draws_3

                self.player.option_1_all3 = self.player.option_1 + self.player.in_round(self.round_number - 2).option_1 + self.player.in_round(self.round_number - 1).option_1
                self.player.option_2_all3 = self.player.option_2 + self.player.in_round(self.round_number - 2).option_2 + self.player.in_round(self.round_number - 1).option_2
                self.player.option_3_all3 = self.player.option_3 + self.player.in_round(self.round_number - 2).option_3 + self.player.in_round(self.round_number - 1).option_3

            else:
                pass

        elif not self.participant.vars['choice'] and not self.participant.vars['safe'] and not self.participant.vars['variance']:

            Urn_1 = ['0', '1', '2', '3', '4', '5', '6', '7']
            Urn_2 = ['-9', '-5', '-4', '-3', '35', '40', '50', '60']
            Urn_3 = ['2', '4']

            weights_1 = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
            weights_2 = [0.2, 0.2, 0.2, 0.2, 0.05, 0.05, 0.05, 0.05]
            weights_3 = [0.5, 0.5]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str

            print(self.player.urn_draws_1)
            print(draws_1)
            print(draws_2)
            print(draws_3)

            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)

            print(count_1)
            print(count_2)
            print(count_3)



            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3


            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '0':
                        data_counts[i][k] = v * 0
                    elif k == '1':
                        data_counts[i][k] = v * 1
                    elif k == '2':
                        data_counts[i][k] = v * 2
                    elif k == '3':
                        data_counts[i][k] = v * 3
                    elif k == '4':
                        data_counts[i][k] = v * 4
                    elif k == '5':
                        data_counts[i][k] = v * 5
                    elif k == '6':
                        data_counts[i][k] = v * 6
                    elif k == '7':
                        data_counts[i][k] = v * 7
                    elif k == '8':
                        data_counts[i][k] = v * 8
                    elif k == '9':
                        data_counts[i][k] = v * 9
                    elif k == '10':
                        data_counts[i][k] = v * 10
                    elif k == '20':
                        data_counts[i][k] = v * 20
                    elif k == '25':
                        data_counts[i][k] = v * 25
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40

            self.player.payoff = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    self.player.payoff += values

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        self.player.payoff_1 += v
                    if i == 'count_2':
                        self.player.payoff_2 += v
                    if i == 'count_3':
                        self.player.payoff_3 += v

        self.player.decision_c_page += 1


##no negative draws? Not ready, maybe cut
class PriorsD(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == self.participant.vars['options']['D']

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'draw': self.participant.vars['draw'],
               'sampling': self.participant.vars['sampling'],

               }

class DecisionD1(Page):
    form_model = 'player'

    def is_displayed(self):
        if not self.participant.vars['sampling'] and not self.participant.vars['choice'] and self.player.decision_d_page == 1:
            return self.round_number == self.participant.vars['options']['D']
        elif not self.participant.vars['sampling'] and self.participant.vars['choice'] and self.player.decision_d_page <= 3:
            return self.round_number == self.participant.vars['options']['D']


    def get_form_fields(self):
        if self.participant.vars['choice'] and not self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3']

        elif self.participant.vars['choice'] and self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3', 'option_safe']

        elif not self.participant.vars['choice'] and not self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3']

        elif not self.participant.vars['choice'] and self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3', 'option_safe']

    def error_message(self, values):
        if self.participant.vars['choice'] and not self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] < 1:
                return 'You have to use your point to choose an urn.'
            elif values['option_1'] + values['option_2'] + values['option_3'] > 1:
                return 'You can only choose one option per round.'

        elif self.participant.vars['choice'] and self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] < 1:
                return 'You have to use your point to choose an urn.'
            elif values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] > 1:
                return 'You can only choose one option per round.'

        elif not self.participant.vars['choice'] and not self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] < 3:
                return 'You have to use all three points'
            elif values['option_1'] + values['option_2'] + values['option_3'] > 3:
                return 'You can only use three points per round'

        elif not self.participant.vars['choice'] and self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] < 3:
                return 'You have to use all three points'
            elif values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] > 3:
                return 'You can only use three points per round'

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'safe_option': Constants.safe_option,
               'endowment_choice': Constants.endowment_choice,
               'endowment_points': Constants.endowment_points,
               'safe': self.participant.vars['safe'],
               'draw': self.participant.vars['draw'],
               'sampling': self.participant.vars['sampling'],
               'payoff': self.participant.payoff,
               'points_sampling': self.participant.vars['points_sampling'],
               'sampling_round': self.participant.vars['sampling_round'],

               }

    def before_next_page(self):

        if self.participant.vars['choice'] and not self.participant.vars['safe'] and not self.participant.vars['variance']:

            Urn_1 = ['3', '4', '5', '6', '7', '8', '9', '10']
            Urn_2 = ['0', '1', '2', '3', '20', '25', '35', '40']
            Urn_3 = ['6']

            weights_1 = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
            weights_2 = [0.25, 0.25, 0.15, 0.15, 0.05, 0.05, 0.05, 0.05]
            weights_3 = [1]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str


            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)

            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3

            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '0':
                        data_counts[i][k] = v * 0
                    elif k == '1':
                        data_counts[i][k] = v * 1
                    elif k == '2':
                        data_counts[i][k] = v * 2
                    elif k == '3':
                        data_counts[i][k] = v * 3
                    elif k == '4':
                        data_counts[i][k] = v * 4
                    elif k == '5':
                        data_counts[i][k] = v * 5
                    elif k == '6':
                        data_counts[i][k] = v * 6
                    elif k == '7':
                        data_counts[i][k] = v * 7
                    elif k == '8':
                        data_counts[i][k] = v * 8
                    elif k == '9':
                        data_counts[i][k] = v * 9
                    elif k == '10':
                        data_counts[i][k] = v * 10
                    elif k == '20':
                        data_counts[i][k] = v * 20
                    elif k == '25':
                        data_counts[i][k] = v * 25
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40

            self.player.payoff = 0
            payoffs = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    payoffs += values

            self.player.payoff = payoffs

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0

            payoffs_1 = 0
            payoffs_2 = 0
            payoffs_3 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        payoffs_1 += v
                    if i == 'count_2':
                        payoffs_2 += v
                    if i == 'count_3':
                        payoffs_3 += v

            self.player.payoff_1 = payoffs_1
            self.player.payoff_2 = payoffs_2
            self.player.payoff_3 = payoffs_3

            if (self.round_number - self.participant.vars['sampling_round']) % 2 == 0 and self.round_number >2:
                self.player.payoff_1_m2 = self.player.in_round(self.round_number - 2).payoff_1
                self.player.payoff_2_m2 = self.player.in_round(self.round_number - 2).payoff_2
                self.player.payoff_3_m2 = self.player.in_round(self.round_number - 2).payoff_3

                self.player.payoff_1_m1 = self.player.in_round(self.round_number - 1).payoff_1
                self.player.payoff_2_m1 = self.player.in_round(self.round_number - 1).payoff_2
                self.player.payoff_3_m1 = self.player.in_round(self.round_number - 1).payoff_3

                self.player.payoff_all3 = self.player.payoff + self.player.in_round(self.round_number - 2).payoff + self.player.in_round(self.round_number - 1).payoff

                self.player.payoff_1_all3 = self.player.payoff_1 + self.player.in_round(self.round_number - 2).payoff_1 + self.player.in_round(self.round_number - 1).payoff_1
                self.player.payoff_2_all3 = self.player.payoff_2 + self.player.in_round(self.round_number - 2).payoff_2 + self.player.in_round(self.round_number - 1).payoff_2
                self.player.payoff_3_all3 = self.player.payoff_3 + self.player.in_round(self.round_number - 2).payoff_3 + self.player.in_round(self.round_number - 1).payoff_3

                self.player.urn_draws_1_m2 = self.player.in_round(self.round_number - 2).urn_draws_1
                self.player.urn_draws_2_m2 = self.player.in_round(self.round_number - 2).urn_draws_2
                self.player.urn_draws_3_m2 = self.player.in_round(self.round_number - 2).urn_draws_3

                self.player.urn_draws_1_m1 = self.player.in_round(self.round_number - 1).urn_draws_1
                self.player.urn_draws_2_m1 = self.player.in_round(self.round_number - 1).urn_draws_2
                self.player.urn_draws_3_m1 = self.player.in_round(self.round_number - 1).urn_draws_3

                self.player.option_1_all3 = self.player.option_1 + self.player.in_round(self.round_number - 2).option_1 + self.player.in_round(self.round_number - 1).option_1
                self.player.option_2_all3 = self.player.option_2 + self.player.in_round(self.round_number - 2).option_2 + self.player.in_round(self.round_number - 1).option_2
                self.player.option_3_all3 = self.player.option_3 + self.player.in_round(self.round_number - 2).option_3 + self.player.in_round(self.round_number - 1).option_3

            else:
                pass

        elif not self.participant.vars['choice'] and not self.participant.vars['safe'] and not self.participant.vars['variance']:

            Urn_1 = ['3', '4', '5', '6', '7', '8', '9', '10']
            Urn_2 = ['0', '1', '2', '3', '20', '25', '35', '40']
            Urn_3 = ['6']

            weights_1 = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
            weights_2 = [0.25, 0.25, 0.15, 0.15, 0.05, 0.05, 0.05, 0.05]
            weights_3 = [1]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str

            print(self.player.urn_draws_1)
            print(draws_1)
            print(draws_2)
            print(draws_3)

            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)

            print(count_1)
            print(count_2)
            print(count_3)



            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3


            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '0':
                        data_counts[i][k] = v * 0
                    elif k == '1':
                        data_counts[i][k] = v * 1
                    elif k == '2':
                        data_counts[i][k] = v * 2
                    elif k == '3':
                        data_counts[i][k] = v * 3
                    elif k == '4':
                        data_counts[i][k] = v * 4
                    elif k == '5':
                        data_counts[i][k] = v * 5
                    elif k == '6':
                        data_counts[i][k] = v * 6
                    elif k == '7':
                        data_counts[i][k] = v * 7
                    elif k == '8':
                        data_counts[i][k] = v * 8
                    elif k == '9':
                        data_counts[i][k] = v * 9
                    elif k == '10':
                        data_counts[i][k] = v * 10
                    elif k == '20':
                        data_counts[i][k] = v * 20
                    elif k == '25':
                        data_counts[i][k] = v * 25
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40

            self.player.payoff = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    self.player.payoff += values

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        self.player.payoff_1 += v
                    if i == 'count_2':
                        self.player.payoff_2 += v
                    if i == 'count_3':
                        self.player.payoff_3 += v

        self.player.decision_d_page += 1


##crazy differences
class PriorsE(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == self.participant.vars['options']['D']

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'draw': self.participant.vars['draw'],
               'sampling': self.participant.vars['sampling'],

               }

class DecisionE1(Page):
    form_model = 'player'

    def is_displayed(self):
        if not self.participant.vars['sampling'] and not self.participant.vars['choice'] and self.player.decision_e_page == 1:
            return self.round_number == self.participant.vars['options']['E']
        elif not self.participant.vars['sampling'] and self.participant.vars['choice'] and self.player.decision_e_page <= 3:
            return self.round_number == self.participant.vars['options']['E']


    def get_form_fields(self):
        if self.participant.vars['choice'] and not self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3']

        elif self.participant.vars['choice'] and self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3', 'option_safe']

        elif not self.participant.vars['choice'] and not self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3']

        elif not self.participant.vars['choice'] and self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3', 'option_safe']

    def error_message(self, values):
        if self.participant.vars['choice'] and not self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] < 1:
                return 'You have to use your point to choose an urn.'
            elif values['option_1'] + values['option_2'] + values['option_3'] > 1:
                return 'You can only choose one option per round.'

        elif self.participant.vars['choice'] and self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] < 1:
                return 'You have to use your point to choose an urn.'
            elif values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] > 1:
                return 'You can only choose one option per round.'

        elif not self.participant.vars['choice'] and not self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] < 3:
                return 'You have to use all three points'
            elif values['option_1'] + values['option_2'] + values['option_3'] > 3:
                return 'You can only use three points per round'

        elif not self.participant.vars['choice'] and self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] < 3:
                return 'You have to use all three points'
            elif values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] > 3:
                return 'You can only use three points per round'

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'safe_option': Constants.safe_option,
               'endowment_choice': Constants.endowment_choice,
               'endowment_points': Constants.endowment_points,
               'safe': self.participant.vars['safe'],
               'draw': self.participant.vars['draw'],
               'sampling': self.participant.vars['sampling'],
               'payoff': self.participant.payoff,
               'points_sampling': self.participant.vars['points_sampling'],
               'sampling_round': self.participant.vars['sampling_round'],

               }

    def before_next_page(self):

        if self.participant.vars['choice'] and not self.participant.vars['safe'] and not self.participant.vars['variance']:

            Urn_1 = ['0', '1', '2', '3', '4', '5', '6', '7']
            Urn_2 = ['-19', '-5', '-4', '-3', '35', '40', '50', '100']
            Urn_3 = ['2', '4']

            weights_1 = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
            weights_2 = [0.2, 0.2, 0.2, 0.2, 0.05, 0.05, 0.05, 0.05]
            weights_3 = [0.5, 0.5]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str


            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)

            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3

            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '0':
                        data_counts[i][k] = v * 0
                    elif k == '1':
                        data_counts[i][k] = v * 1
                    elif k == '2':
                        data_counts[i][k] = v * 2
                    elif k == '3':
                        data_counts[i][k] = v * 3
                    elif k == '4':
                        data_counts[i][k] = v * 4
                    elif k == '5':
                        data_counts[i][k] = v * 5
                    elif k == '6':
                        data_counts[i][k] = v * 6
                    elif k == '7':
                        data_counts[i][k] = v * 7
                    elif k == '8':
                        data_counts[i][k] = v * 8
                    elif k == '9':
                        data_counts[i][k] = v * 9
                    elif k == '10':
                        data_counts[i][k] = v * 10
                    elif k == '20':
                        data_counts[i][k] = v * 20
                    elif k == '25':
                        data_counts[i][k] = v * 25
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40

            self.player.payoff = 0
            payoffs = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    payoffs += values

            self.player.payoff = payoffs

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0

            payoffs_1 = 0
            payoffs_2 = 0
            payoffs_3 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        payoffs_1 += v
                    if i == 'count_2':
                        payoffs_2 += v
                    if i == 'count_3':
                        payoffs_3 += v

            self.player.payoff_1 = payoffs_1
            self.player.payoff_2 = payoffs_2
            self.player.payoff_3 = payoffs_3

            if (self.round_number - self.participant.vars['sampling_round']) % 2 == 0 and self.round_number >2:
                self.player.payoff_1_m2 = self.player.in_round(self.round_number - 2).payoff_1
                self.player.payoff_2_m2 = self.player.in_round(self.round_number - 2).payoff_2
                self.player.payoff_3_m2 = self.player.in_round(self.round_number - 2).payoff_3

                self.player.payoff_1_m1 = self.player.in_round(self.round_number - 1).payoff_1
                self.player.payoff_2_m1 = self.player.in_round(self.round_number - 1).payoff_2
                self.player.payoff_3_m1 = self.player.in_round(self.round_number - 1).payoff_3

                self.player.payoff_all3 = self.player.payoff + self.player.in_round(self.round_number - 2).payoff + self.player.in_round(self.round_number - 1).payoff

                self.player.payoff_1_all3 = self.player.payoff_1 + self.player.in_round(self.round_number - 2).payoff_1 + self.player.in_round(self.round_number - 1).payoff_1
                self.player.payoff_2_all3 = self.player.payoff_2 + self.player.in_round(self.round_number - 2).payoff_2 + self.player.in_round(self.round_number - 1).payoff_2
                self.player.payoff_3_all3 = self.player.payoff_3 + self.player.in_round(self.round_number - 2).payoff_3 + self.player.in_round(self.round_number - 1).payoff_3

                self.player.urn_draws_1_m2 = self.player.in_round(self.round_number - 2).urn_draws_1
                self.player.urn_draws_2_m2 = self.player.in_round(self.round_number - 2).urn_draws_2
                self.player.urn_draws_3_m2 = self.player.in_round(self.round_number - 2).urn_draws_3

                self.player.urn_draws_1_m1 = self.player.in_round(self.round_number - 1).urn_draws_1
                self.player.urn_draws_2_m1 = self.player.in_round(self.round_number - 1).urn_draws_2
                self.player.urn_draws_3_m1 = self.player.in_round(self.round_number - 1).urn_draws_3

                self.player.option_1_all3 = self.player.option_1 + self.player.in_round(self.round_number - 2).option_1 + self.player.in_round(self.round_number - 1).option_1
                self.player.option_2_all3 = self.player.option_2 + self.player.in_round(self.round_number - 2).option_2 + self.player.in_round(self.round_number - 1).option_2
                self.player.option_3_all3 = self.player.option_3 + self.player.in_round(self.round_number - 2).option_3 + self.player.in_round(self.round_number - 1).option_3

            else:
                pass

        elif not self.participant.vars['choice'] and not self.participant.vars['safe'] and not self.participant.vars['variance']:

            Urn_1 = ['0', '1', '2', '3', '4', '5', '6', '7']
            Urn_2 = ['-19', '-5', '-4', '-3', '35', '40', '50', '100']
            Urn_3 = ['2', '4']

            weights_1 = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
            weights_2 = [0.2, 0.2, 0.2, 0.2, 0.05, 0.05, 0.05, 0.05]
            weights_3 = [0.5, 0.5]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str

            print(self.player.urn_draws_1)
            print(draws_1)
            print(draws_2)
            print(draws_3)

            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)

            print(count_1)
            print(count_2)
            print(count_3)



            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3


            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '0':
                        data_counts[i][k] = v * 0
                    elif k == '1':
                        data_counts[i][k] = v * 1
                    elif k == '2':
                        data_counts[i][k] = v * 2
                    elif k == '3':
                        data_counts[i][k] = v * 3
                    elif k == '4':
                        data_counts[i][k] = v * 4
                    elif k == '5':
                        data_counts[i][k] = v * 5
                    elif k == '6':
                        data_counts[i][k] = v * 6
                    elif k == '7':
                        data_counts[i][k] = v * 7
                    elif k == '8':
                        data_counts[i][k] = v * 8
                    elif k == '9':
                        data_counts[i][k] = v * 9
                    elif k == '10':
                        data_counts[i][k] = v * 10
                    elif k == '20':
                        data_counts[i][k] = v * 20
                    elif k == '25':
                        data_counts[i][k] = v * 25
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40

            self.player.payoff = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    self.player.payoff += values

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        self.player.payoff_1 += v
                    if i == 'count_2':
                        self.player.payoff_2 += v
                    if i == 'count_3':
                        self.player.payoff_3 += v

        self.player.decision_e_page += 1


##change in priors

class PriorsTransition_2(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == self.participant.vars['options']['F']

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'draw': self.participant.vars['draw'],
               'sampling': self.participant.vars['sampling'],

               }

class PriorsF1(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == self.participant.vars['options']['F']

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'draw': self.participant.vars['draw'],
               'sampling': self.participant.vars['sampling'],

               }

class DecisionF1(Page):
    form_model = 'player'

    def is_displayed(self):
        if not self.participant.vars['sampling'] and not self.participant.vars['choice'] and self.player.decision_f_page == 1:
            return self.round_number == self.participant.vars['options']['F']
        elif not self.participant.vars['sampling'] and self.participant.vars['choice'] and self.player.decision_f_page <= 3:
            return self.round_number == self.participant.vars['options']['F']


    def get_form_fields(self):
        if self.participant.vars['choice'] and not self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3']

        elif self.participant.vars['choice'] and self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3', 'option_safe']

        elif not self.participant.vars['choice'] and not self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3']

        elif not self.participant.vars['choice'] and self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3', 'option_safe']

    def error_message(self, values):
        if self.participant.vars['choice'] and not self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] < 1:
                return 'You have to use your point to choose an urn.'
            elif values['option_1'] + values['option_2'] + values['option_3'] > 1:
                return 'You can only choose one option per round.'

        elif self.participant.vars['choice'] and self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] < 1:
                return 'You have to use your point to choose an urn.'
            elif values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] > 1:
                return 'You can only choose one option per round.'

        elif not self.participant.vars['choice'] and not self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] < 3:
                return 'You have to use all three points'
            elif values['option_1'] + values['option_2'] + values['option_3'] > 3:
                return 'You can only use three points per round'

        elif not self.participant.vars['choice'] and self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] < 3:
                return 'You have to use all three points'
            elif values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] > 3:
                return 'You can only use three points per round'

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'safe_option': Constants.safe_option,
               'endowment_choice': Constants.endowment_choice,
               'endowment_points': Constants.endowment_points,
               'safe': self.participant.vars['safe'],
               'draw': self.participant.vars['draw'],
               'sampling': self.participant.vars['sampling'],
               'payoff': self.participant.payoff,
               'points_sampling': self.participant.vars['points_sampling'],
               'sampling_round': self.participant.vars['sampling_round'],

               }

    def before_next_page(self):

        if self.participant.vars['choice'] and not self.participant.vars['safe'] and not self.participant.vars['variance']:

            Urn_1 = ['0', '1', '2', '3', '4', '5', '6', '7']
            Urn_2 = ['-19', '-5', '-4', '-3', '35', '40', '50', '100']
            Urn_3 = ['2', '4']

            weights_1 = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
            weights_2 = [0.2, 0.2, 0.2, 0.2, 0.05, 0.05, 0.05, 0.05]
            weights_3 = [0.5, 0.5]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str


            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)

            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3

            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '0':
                        data_counts[i][k] = v * 0
                    elif k == '1':
                        data_counts[i][k] = v * 1
                    elif k == '2':
                        data_counts[i][k] = v * 2
                    elif k == '3':
                        data_counts[i][k] = v * 3
                    elif k == '4':
                        data_counts[i][k] = v * 4
                    elif k == '5':
                        data_counts[i][k] = v * 5
                    elif k == '6':
                        data_counts[i][k] = v * 6
                    elif k == '7':
                        data_counts[i][k] = v * 7
                    elif k == '8':
                        data_counts[i][k] = v * 8
                    elif k == '9':
                        data_counts[i][k] = v * 9
                    elif k == '10':
                        data_counts[i][k] = v * 10
                    elif k == '20':
                        data_counts[i][k] = v * 20
                    elif k == '25':
                        data_counts[i][k] = v * 25
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40

            self.player.payoff = 0
            payoffs = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    payoffs += values

            self.player.payoff = payoffs

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0

            payoffs_1 = 0
            payoffs_2 = 0
            payoffs_3 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        payoffs_1 += v
                    if i == 'count_2':
                        payoffs_2 += v
                    if i == 'count_3':
                        payoffs_3 += v

            self.player.payoff_1 = payoffs_1
            self.player.payoff_2 = payoffs_2
            self.player.payoff_3 = payoffs_3

            if (self.round_number - self.participant.vars['sampling_round']) % 2 == 0 and self.round_number >2:
                self.player.payoff_1_m2 = self.player.in_round(self.round_number - 2).payoff_1
                self.player.payoff_2_m2 = self.player.in_round(self.round_number - 2).payoff_2
                self.player.payoff_3_m2 = self.player.in_round(self.round_number - 2).payoff_3

                self.player.payoff_1_m1 = self.player.in_round(self.round_number - 1).payoff_1
                self.player.payoff_2_m1 = self.player.in_round(self.round_number - 1).payoff_2
                self.player.payoff_3_m1 = self.player.in_round(self.round_number - 1).payoff_3

                self.player.payoff_all3 = self.player.payoff + self.player.in_round(self.round_number - 2).payoff + self.player.in_round(self.round_number - 1).payoff

                self.player.payoff_1_all3 = self.player.payoff_1 + self.player.in_round(self.round_number - 2).payoff_1 + self.player.in_round(self.round_number - 1).payoff_1
                self.player.payoff_2_all3 = self.player.payoff_2 + self.player.in_round(self.round_number - 2).payoff_2 + self.player.in_round(self.round_number - 1).payoff_2
                self.player.payoff_3_all3 = self.player.payoff_3 + self.player.in_round(self.round_number - 2).payoff_3 + self.player.in_round(self.round_number - 1).payoff_3

                self.player.urn_draws_1_m2 = self.player.in_round(self.round_number - 2).urn_draws_1
                self.player.urn_draws_2_m2 = self.player.in_round(self.round_number - 2).urn_draws_2
                self.player.urn_draws_3_m2 = self.player.in_round(self.round_number - 2).urn_draws_3

                self.player.urn_draws_1_m1 = self.player.in_round(self.round_number - 1).urn_draws_1
                self.player.urn_draws_2_m1 = self.player.in_round(self.round_number - 1).urn_draws_2
                self.player.urn_draws_3_m1 = self.player.in_round(self.round_number - 1).urn_draws_3

                self.player.option_1_all3 = self.player.option_1 + self.player.in_round(self.round_number - 2).option_1 + self.player.in_round(self.round_number - 1).option_1
                self.player.option_2_all3 = self.player.option_2 + self.player.in_round(self.round_number - 2).option_2 + self.player.in_round(self.round_number - 1).option_2
                self.player.option_3_all3 = self.player.option_3 + self.player.in_round(self.round_number - 2).option_3 + self.player.in_round(self.round_number - 1).option_3

            else:
                pass

        elif not self.participant.vars['choice'] and not self.participant.vars['safe'] and not self.participant.vars['variance']:

            Urn_1 = ['0', '1', '2', '3', '4', '5', '6', '7']
            Urn_2 = ['-19', '-5', '-4', '-3', '35', '40', '50', '100']
            Urn_3 = ['2', '4']

            weights_1 = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
            weights_2 = [0.2, 0.2, 0.2, 0.2, 0.05, 0.05, 0.05, 0.05]
            weights_3 = [0.5, 0.5]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str

            print(self.player.urn_draws_1)
            print(draws_1)
            print(draws_2)
            print(draws_3)

            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)

            print(count_1)
            print(count_2)
            print(count_3)



            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3


            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '0':
                        data_counts[i][k] = v * 0
                    elif k == '1':
                        data_counts[i][k] = v * 1
                    elif k == '2':
                        data_counts[i][k] = v * 2
                    elif k == '3':
                        data_counts[i][k] = v * 3
                    elif k == '4':
                        data_counts[i][k] = v * 4
                    elif k == '5':
                        data_counts[i][k] = v * 5
                    elif k == '6':
                        data_counts[i][k] = v * 6
                    elif k == '7':
                        data_counts[i][k] = v * 7
                    elif k == '8':
                        data_counts[i][k] = v * 8
                    elif k == '9':
                        data_counts[i][k] = v * 9
                    elif k == '10':
                        data_counts[i][k] = v * 10
                    elif k == '20':
                        data_counts[i][k] = v * 20
                    elif k == '25':
                        data_counts[i][k] = v * 25
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40

            self.player.payoff = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    self.player.payoff += values

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        self.player.payoff_1 += v
                    if i == 'count_2':
                        self.player.payoff_2 += v
                    if i == 'count_3':
                        self.player.payoff_3 += v

        self.player.decision_f_page += 1

class PriorsF2(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == self.participant.vars['options']['F']

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'draw': self.participant.vars['draw'],
               'sampling': self.participant.vars['sampling'],

               }

class DecisionF2(Page):
    form_model = 'player'

    def is_displayed(self):
        if not self.participant.vars['sampling'] and not self.participant.vars['choice'] and self.player.decision_f2_page == 1:
            return self.round_number == self.participant.vars['options']['F']
        elif not self.participant.vars['sampling'] and self.participant.vars['choice'] and self.player.decision_f2_page <= 3:
            return self.round_number == self.participant.vars['options']['F']


    def get_form_fields(self):
        if self.participant.vars['choice'] and not self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3']

        elif self.participant.vars['choice'] and self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3', 'option_safe']

        elif not self.participant.vars['choice'] and not self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3']

        elif not self.participant.vars['choice'] and self.participant.vars['safe']:
            return ['option_1', 'option_2', 'option_3', 'option_safe']

    def error_message(self, values):
        if self.participant.vars['choice'] and not self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] < 1:
                return 'You have to use your point to choose an urn.'
            elif values['option_1'] + values['option_2'] + values['option_3'] > 1:
                return 'You can only choose one option per round.'

        elif self.participant.vars['choice'] and self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] < 1:
                return 'You have to use your point to choose an urn.'
            elif values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] > 1:
                return 'You can only choose one option per round.'

        elif not self.participant.vars['choice'] and not self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] < 3:
                return 'You have to use all three points'
            elif values['option_1'] + values['option_2'] + values['option_3'] > 3:
                return 'You can only use three points per round'

        elif not self.participant.vars['choice'] and self.participant.vars['safe']:
            if values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] < 3:
                return 'You have to use all three points'
            elif values['option_1'] + values['option_2'] + values['option_3'] + values['option_safe'] > 3:
                return 'You can only use three points per round'

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'safe_option': Constants.safe_option,
               'endowment_choice': Constants.endowment_choice,
               'endowment_points': Constants.endowment_points,
               'safe': self.participant.vars['safe'],
               'draw': self.participant.vars['draw'],
               'sampling': self.participant.vars['sampling'],
               'payoff': self.participant.payoff,
               'points_sampling': self.participant.vars['points_sampling'],
               'sampling_round': self.participant.vars['sampling_round'],

               }

    def before_next_page(self):

        if self.participant.vars['choice'] and not self.participant.vars['safe'] and not self.participant.vars['variance']:

            Urn_1 = ['0', '1', '2', '3', '4', '5', '6', '7']
            Urn_2 = ['-19', '-5', '-4', '-3', '35', '40', '50', '100']
            Urn_3 = ['2', '4']

            weights_1 = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
            weights_2 = [0.2, 0.2, 0.2, 0.2, 0.05, 0.05, 0.05, 0.05]
            weights_3 = [0.5, 0.5]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str


            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)

            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3

            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '0':
                        data_counts[i][k] = v * 0
                    elif k == '1':
                        data_counts[i][k] = v * 1
                    elif k == '2':
                        data_counts[i][k] = v * 2
                    elif k == '3':
                        data_counts[i][k] = v * 3
                    elif k == '4':
                        data_counts[i][k] = v * 4
                    elif k == '5':
                        data_counts[i][k] = v * 5
                    elif k == '6':
                        data_counts[i][k] = v * 6
                    elif k == '7':
                        data_counts[i][k] = v * 7
                    elif k == '8':
                        data_counts[i][k] = v * 8
                    elif k == '9':
                        data_counts[i][k] = v * 9
                    elif k == '10':
                        data_counts[i][k] = v * 10
                    elif k == '20':
                        data_counts[i][k] = v * 20
                    elif k == '25':
                        data_counts[i][k] = v * 25
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40

            self.player.payoff = 0
            payoffs = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    payoffs += values

            self.player.payoff = payoffs

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0

            payoffs_1 = 0
            payoffs_2 = 0
            payoffs_3 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        payoffs_1 += v
                    if i == 'count_2':
                        payoffs_2 += v
                    if i == 'count_3':
                        payoffs_3 += v

            self.player.payoff_1 = payoffs_1
            self.player.payoff_2 = payoffs_2
            self.player.payoff_3 = payoffs_3

            if (self.round_number - self.participant.vars['sampling_round']) % 2 == 0 and self.round_number >2:
                self.player.payoff_1_m2 = self.player.in_round(self.round_number - 2).payoff_1
                self.player.payoff_2_m2 = self.player.in_round(self.round_number - 2).payoff_2
                self.player.payoff_3_m2 = self.player.in_round(self.round_number - 2).payoff_3

                self.player.payoff_1_m1 = self.player.in_round(self.round_number - 1).payoff_1
                self.player.payoff_2_m1 = self.player.in_round(self.round_number - 1).payoff_2
                self.player.payoff_3_m1 = self.player.in_round(self.round_number - 1).payoff_3

                self.player.payoff_all3 = self.player.payoff + self.player.in_round(self.round_number - 2).payoff + self.player.in_round(self.round_number - 1).payoff

                self.player.payoff_1_all3 = self.player.payoff_1 + self.player.in_round(self.round_number - 2).payoff_1 + self.player.in_round(self.round_number - 1).payoff_1
                self.player.payoff_2_all3 = self.player.payoff_2 + self.player.in_round(self.round_number - 2).payoff_2 + self.player.in_round(self.round_number - 1).payoff_2
                self.player.payoff_3_all3 = self.player.payoff_3 + self.player.in_round(self.round_number - 2).payoff_3 + self.player.in_round(self.round_number - 1).payoff_3

                self.player.urn_draws_1_m2 = self.player.in_round(self.round_number - 2).urn_draws_1
                self.player.urn_draws_2_m2 = self.player.in_round(self.round_number - 2).urn_draws_2
                self.player.urn_draws_3_m2 = self.player.in_round(self.round_number - 2).urn_draws_3

                self.player.urn_draws_1_m1 = self.player.in_round(self.round_number - 1).urn_draws_1
                self.player.urn_draws_2_m1 = self.player.in_round(self.round_number - 1).urn_draws_2
                self.player.urn_draws_3_m1 = self.player.in_round(self.round_number - 1).urn_draws_3

                self.player.option_1_all3 = self.player.option_1 + self.player.in_round(self.round_number - 2).option_1 + self.player.in_round(self.round_number - 1).option_1
                self.player.option_2_all3 = self.player.option_2 + self.player.in_round(self.round_number - 2).option_2 + self.player.in_round(self.round_number - 1).option_2
                self.player.option_3_all3 = self.player.option_3 + self.player.in_round(self.round_number - 2).option_3 + self.player.in_round(self.round_number - 1).option_3

            else:
                pass

        elif not self.participant.vars['choice'] and not self.participant.vars['safe'] and not self.participant.vars['variance']:

            Urn_1 = ['0', '1', '2', '3', '4', '5', '6', '7']
            Urn_2 = ['-19', '-5', '-4', '-3', '35', '40', '50', '100']
            Urn_3 = ['2', '4']

            weights_1 = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
            weights_2 = [0.2, 0.2, 0.2, 0.2, 0.05, 0.05, 0.05, 0.05]
            weights_3 = [0.5, 0.5]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str

            print(self.player.urn_draws_1)
            print(draws_1)
            print(draws_2)
            print(draws_3)

            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)

            print(count_1)
            print(count_2)
            print(count_3)



            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3


            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '0':
                        data_counts[i][k] = v * 0
                    elif k == '1':
                        data_counts[i][k] = v * 1
                    elif k == '2':
                        data_counts[i][k] = v * 2
                    elif k == '3':
                        data_counts[i][k] = v * 3
                    elif k == '4':
                        data_counts[i][k] = v * 4
                    elif k == '5':
                        data_counts[i][k] = v * 5
                    elif k == '6':
                        data_counts[i][k] = v * 6
                    elif k == '7':
                        data_counts[i][k] = v * 7
                    elif k == '8':
                        data_counts[i][k] = v * 8
                    elif k == '9':
                        data_counts[i][k] = v * 9
                    elif k == '10':
                        data_counts[i][k] = v * 10
                    elif k == '20':
                        data_counts[i][k] = v * 20
                    elif k == '25':
                        data_counts[i][k] = v * 25
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40

            self.player.payoff = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    self.player.payoff += values

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        self.player.payoff_1 += v
                    if i == 'count_2':
                        self.player.payoff_2 += v
                    if i == 'count_3':
                        self.player.payoff_3 += v

        self.player.decision_f2_page += 1


class Feedback(Page):
    form_model = 'player'

    def is_displayed(self):
        if self.participant.vars['choice'] and not self.participant.vars['sampling']:
            return self.round_number <= Constants.num_rounds_choice
        elif not self.participant.vars['choice'] and not self.participant.vars['sampling']:
            return self.round_number <= Constants.num_rounds_points


    def vars_for_template(self):
        return {'payoff': self.player.payoff,
                'payoff_1': self.player.payoff_1,
                'payoff_2': self.player.payoff_2,
                'payoff_3': self.player.payoff_3,
                'choice': self.participant.vars['choice'],
                'urn_draws_1': self.player.urn_draws_1,
                'urn_draws_2': self.player.urn_draws_2,
                'urn_draws_3': self.player.urn_draws_3,
                'urn_draws_4': self.player.urn_draws_4,
                'payoff_4': self.player.payoff_4,
                'safe': self.participant.vars['safe'],
                'draw': self.participant.vars['draw'],
                'feedback_3': self.participant.vars['feedback_3'],
                }


########################################################################################################################
# Questionnaire and Final Page #########################################################################################
########################################################################################################################


class Questionnaire(Page):
    form_model ='player'

    def get_form_fields(self):
        if self.player.questionnaire_page == 1:
            return []
        elif self.player.questionnaire_page == 2:
            return ['q_risk']
        elif self.player.questionnaire_page == 3:
            return ['q_exploration_strategy']
        elif self.player.questionnaire_page == 4 and self.participant.vars['choice']:
            return ['q_mean_sequential', 'q_sd_sequential', 'q_ld_sequential', 'q_hd_sequential', 'q_descr_exp']
        elif self.player.questionnaire_page == 4 and not self.participant.vars['choice']:
            return ['q_mean_simultan', 'q_sd_simultan', 'q_ld_simultan', 'q_hd_simultan', 'q_descr_exp']
        elif self.player.questionnaire_page == 5:
            epo = [f'q_epo_{i}' for i in range(1, 14)]
            return epo
        elif self.player.questionnaire_page == 6:
            return ['q_year', 'q_sex', 'q_employment', 'q_education',
                    'q_ethnicity']


    def is_displayed(self):
        if self.participant.vars['choice']:
            return self.round_number == Constants.num_rounds_choice
        else:
            return self.round_number == Constants.num_rounds_points

    def vars_for_template(self):
        return{'questionnaire_page': self.player.questionnaire_page,
               'choice':self.participant.vars['choice'],
               'safe': self.participant.vars['safe'],
               'round': self.player.round_number,

               }

    def before_next_page(self):
        self.player.questionnaire_page += 1


class FinalInfo(Page):
    def is_displayed(self):
        if self.participant.vars['choice']:
            return self.round_number == Constants.num_rounds_choice
        else:
            return self.round_number == Constants.num_rounds_points

    def vars_for_template(self):
        return {'participation_fee': self.session.config['participation_fee'],
                'total_payoff': self.participant.vars['total_payoff'],
                'bonus': self.participant.vars['bonus'],
                'completion_code': self.participant.vars['completion_code'],
                }



page_sequence = [
    #DecisionTransition,
    PriorsA,
    DecisionA1,
    PriorsB,
    DecisionB1,
    PriorsC,
    DecisionC1,
    PriorsD,
    DecisionD1,
    PriorsE,
    DecisionE1,
    PriorsF1,
    DecisionF1,
    PriorsF2,
    DecisionF2,
    Feedback,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    FinalInfo,
]
