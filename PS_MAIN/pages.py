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

    def before_next_page(self):
        self.participant.payoff = 10


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
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40
                    elif k == '50':
                        data_counts[i][k] = v * 50
                    elif k == '60':
                        data_counts[i][k] = v * 60
                    elif k == '-9':
                        data_counts[i][k] = v * -9
                    elif k == '-5':
                        data_counts[i][k] = v * -5
                    elif k == '-4':
                        data_counts[i][k] = v * -4
                    elif k == '-3':
                        data_counts[i][k] = v * -3

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

            if self.player.decision_a_page == 1:
                self.participant.vars['payoff_a1_1'] = self.player.payoff = payoffs
                self.participant.vars['urndraws1_a1_1'] = self.player.urn_draws_1
                self.participant.vars['urndraws2_a1_1'] = self.player.urn_draws_2
                self.participant.vars['urndraws3_a1_1'] = self.player.urn_draws_3
                self.participant.vars['option_1_a1_1'] = self.player.option_1
                self.participant.vars['option_2_a1_1'] = self.player.option_2
                self.participant.vars['option_3_a1_1'] = self.player.option_3

                self.participant.vars['payoff_1_a_1'] = self.player.payoff_1
                self.participant.vars['payoff_2_a_1'] = self.player.payoff_2
                self.participant.vars['payoff_3_a_1'] = self.player.payoff_3

                self.player.option_1 = 0
                self.player.option_2 = 0
                self.player.option_3 = 0

            if self.player.decision_a_page == 2:
                self.participant.vars['payoff_a1_2'] = self.player.payoff = payoffs
                self.participant.vars['urndraws1_a1_2'] = self.player.urn_draws_1
                self.participant.vars['urndraws2_a1_2'] = self.player.urn_draws_2
                self.participant.vars['urndraws3_a1_2'] = self.player.urn_draws_3
                self.participant.vars['option_1_a1_2'] = self.player.option_1
                self.participant.vars['option_2_a1_2'] = self.player.option_2
                self.participant.vars['option_3_a1_2'] = self.player.option_3
                
                self.participant.vars['payoff_1_a_2'] = self.player.payoff_1
                self.participant.vars['payoff_2_a_2'] = self.player.payoff_2
                self.participant.vars['payoff_3_a_2'] = self.player.payoff_3                

                self.player.option_1 = 0
                self.player.option_2 = 0
                self.player.option_3 = 0

            if self.player.decision_a_page == 3:
                self.participant.vars['payoff_a1_3'] = self.player.payoff = payoffs
                self.participant.vars['urndraws1_a1_3'] = self.player.urn_draws_1
                self.participant.vars['urndraws2_a1_3'] = self.player.urn_draws_2
                self.participant.vars['urndraws3_a1_3'] = self.player.urn_draws_3
                self.participant.vars['option_1_a1_3'] = self.player.option_1
                self.participant.vars['option_2_a1_3'] = self.player.option_2
                self.participant.vars['option_3_a1_3'] = self.player.option_3
                
                self.participant.vars['payoff_1_a_3'] = self.player.payoff_1
                self.participant.vars['payoff_2_a_3'] = self.player.payoff_2
                self.participant.vars['payoff_3_a_3'] = self.player.payoff_3

                self.participant.vars['payoff_a1'] = self.participant.vars['payoff_a1_1'] + self.participant.vars['payoff_a1_2'] + self.participant.vars['payoff_a1_3']
                self.participant.vars['urndraws1_a1'] = self.participant.vars['urndraws1_a1_1'] + self.participant.vars['urndraws1_a1_2'] + self.participant.vars['urndraws1_a1_3']
                self.participant.vars['urndraws2_a1'] = self.participant.vars['urndraws2_a1_1'] + self.participant.vars['urndraws2_a1_2'] + self.participant.vars['urndraws2_a1_3']
                self.participant.vars['urndraws3_a1'] = self.participant.vars['urndraws3_a1_1'] + self.participant.vars['urndraws3_a1_2'] + self.participant.vars['urndraws3_a1_3']
                self.participant.vars['option_1_a1'] = self.participant.vars['option_1_a1_1'] + self.participant.vars['option_1_a1_2'] + self.participant.vars['option_1_a1_3']
                self.participant.vars['option_2_a1'] = self.participant.vars['option_2_a1_1'] + self.participant.vars['option_2_a1_2'] + self.participant.vars['option_2_a1_3']
                self.participant.vars['option_3_a1'] = self.participant.vars['option_3_a1_1'] + self.participant.vars['option_3_a1_2'] + self.participant.vars['option_3_a1_3']

                self.participant.vars['payoff_1_a'] = self.participant.vars['payoff_1_a_1'] + self.participant.vars['payoff_1_a_2'] + self.participant.vars['payoff_1_a_3']
                self.participant.vars['payoff_2_a'] = self.participant.vars['payoff_2_a_1'] + self.participant.vars['payoff_2_a_2'] + self.participant.vars['payoff_2_a_3']
                self.participant.vars['payoff_3_a'] = self.participant.vars['payoff_3_a_1'] + self.participant.vars['payoff_3_a_2'] + self.participant.vars['payoff_3_a_3']


        elif not self.participant.vars['choice']:

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
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40
                    elif k == '50':
                        data_counts[i][k] = v * 50
                    elif k == '60':
                        data_counts[i][k] = v * 60
                    elif k == '-9':
                        data_counts[i][k] = v * -9
                    elif k == '-5':
                        data_counts[i][k] = v * -5
                    elif k == '-4':
                        data_counts[i][k] = v * -4
                    elif k == '-3':
                        data_counts[i][k] = v * -3

            self.player.payoff = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    self.player.payoff += values


            self.participant.vars['payoff_a1'] = self.player.payoff
            self.participant.vars['urndraws1_a1'] = self.player.urn_draws_1
            self.participant.vars['urndraws2_a1'] = self.player.urn_draws_2
            self.participant.vars['urndraws3_a1'] = self.player.urn_draws_3
            
            self.participant.vars['option_1_a1'] = self.player.option_1
            self.participant.vars['option_2_a1'] = self.player.option_2
            self.participant.vars['option_3_a1'] = self.player.option_3


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

            self.participant.vars['payoff_1_a'] = self.player.payoff_1
            self.participant.vars['payoff_2_a'] = self.player.payoff_2
            self.participant.vars['payoff_3_a'] = self.player.payoff_3

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

        if self.participant.vars['choice'] and not self.participant.vars['safe']:

            Urn_1 = ['0', '1', '2', '3', '4', '5', '6', '7']
            Urn_2 = ['-9', '-5', '-4', '-3', '35', '40', '50', '50']
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
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40
                    elif k == '50':
                        data_counts[i][k] = v * 50
                    elif k == '60':
                        data_counts[i][k] = v * 60
                    elif k == '-9':
                        data_counts[i][k] = v * -9
                    elif k == '-5':
                        data_counts[i][k] = v * -5
                    elif k == '-4':
                        data_counts[i][k] = v * -4
                    elif k == '-3':
                        data_counts[i][k] = v * -3

            self.player.payoff = 0
            payoffs = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    payoffs += values

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

            if self.player.decision_b_page == 1:
                self.participant.vars['payoff_b1_1'] = self.player.payoff = payoffs
                self.participant.vars['urndraws1_b1_1'] = self.player.urn_draws_1
                self.participant.vars['urndraws2_b1_1'] = self.player.urn_draws_2
                self.participant.vars['urndraws3_b1_1'] = self.player.urn_draws_3
                self.participant.vars['option_1_b1_1'] = self.player.option_1
                self.participant.vars['option_2_b1_1'] = self.player.option_2
                self.participant.vars['option_3_b1_1'] = self.player.option_3

                self.participant.vars['payoff_1_b_1'] = self.player.payoff_1
                self.participant.vars['payoff_2_b_1'] = self.player.payoff_2
                self.participant.vars['payoff_3_b_1'] = self.player.payoff_3

                self.player.option_1 = 0
                self.player.option_2 = 0
                self.player.option_3 = 0

            if self.player.decision_b_page == 2:
                self.participant.vars['payoff_b1_2'] = self.player.payoff = payoffs
                self.participant.vars['urndraws1_b1_2'] = self.player.urn_draws_1
                self.participant.vars['urndraws2_b1_2'] = self.player.urn_draws_2
                self.participant.vars['urndraws3_b1_2'] = self.player.urn_draws_3
                self.participant.vars['option_1_b1_2'] = self.player.option_1
                self.participant.vars['option_2_b1_2'] = self.player.option_2
                self.participant.vars['option_3_b1_2'] = self.player.option_3

                self.participant.vars['payoff_1_b_2'] = self.player.payoff_1
                self.participant.vars['payoff_2_b_2'] = self.player.payoff_2
                self.participant.vars['payoff_3_b_2'] = self.player.payoff_3

                self.player.option_1 = 0
                self.player.option_2 = 0
                self.player.option_3 = 0

            if self.player.decision_b_page == 3:
                self.participant.vars['payoff_b1_3'] = self.player.payoff = payoffs
                self.participant.vars['urndraws1_b1_3'] = self.player.urn_draws_1
                self.participant.vars['urndraws2_b1_3'] = self.player.urn_draws_2
                self.participant.vars['urndraws3_b1_3'] = self.player.urn_draws_3
                self.participant.vars['option_1_b1_3'] = self.player.option_1
                self.participant.vars['option_2_b1_3'] = self.player.option_2
                self.participant.vars['option_3_b1_3'] = self.player.option_3

                self.participant.vars['payoff_1_b_3'] = self.player.payoff_1
                self.participant.vars['payoff_2_b_3'] = self.player.payoff_2
                self.participant.vars['payoff_3_b_3'] = self.player.payoff_3

                self.participant.vars['payoff_b1'] = self.participant.vars['payoff_b1_1'] + self.participant.vars[
                    'payoff_b1_2'] + self.participant.vars['payoff_b1_3']
                self.participant.vars['urndraws1_b1'] = self.participant.vars['urndraws1_b1_1'] + self.participant.vars[
                    'urndraws1_b1_2'] + self.participant.vars['urndraws1_b1_3']
                self.participant.vars['urndraws2_b1'] = self.participant.vars['urndraws2_b1_1'] + self.participant.vars[
                    'urndraws2_b1_2'] + self.participant.vars['urndraws2_b1_3']
                self.participant.vars['urndraws3_b1'] = self.participant.vars['urndraws3_b1_1'] + self.participant.vars[
                    'urndraws3_b1_2'] + self.participant.vars['urndraws3_b1_3']
                self.participant.vars['option_1_b1'] = self.participant.vars['option_1_b1_1'] + self.participant.vars[
                    'option_1_b1_2'] + self.participant.vars['option_1_b1_3']
                self.participant.vars['option_2_b1'] = self.participant.vars['option_2_b1_1'] + self.participant.vars['option_2_b1_2'] + self.participant.vars['option_2_b1_3']
                self.participant.vars['option_3_b1'] = self.participant.vars['option_3_b1_1'] + self.participant.vars['option_3_b1_2'] + self.participant.vars['option_3_b1_3']

                self.participant.vars['payoff_1_b'] = self.participant.vars['payoff_1_b_1'] + self.participant.vars['payoff_1_b_2'] + self.participant.vars['payoff_1_b_3']
                self.participant.vars['payoff_2_b'] = self.participant.vars['payoff_2_b_1'] + self.participant.vars['payoff_2_b_2'] + self.participant.vars['payoff_2_b_3']
                self.participant.vars['payoff_3_b'] = self.participant.vars['payoff_3_b_1'] + self.participant.vars['payoff_3_b_2'] + self.participant.vars['payoff_3_b_3']


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
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40
                    elif k == '50':
                        data_counts[i][k] = v * 50
                    elif k == '60':
                        data_counts[i][k] = v * 60
                    elif k == '-9':
                        data_counts[i][k] = v * -9
                    elif k == '-5':
                        data_counts[i][k] = v * -5
                    elif k == '-4':
                        data_counts[i][k] = v * -4
                    elif k == '-3':
                        data_counts[i][k] = v * -3

            self.player.payoff = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    self.player.payoff += values

            self.participant.vars['payoff_b1'] = self.player.payoff
            self.participant.vars['urndraws1_b1'] = self.player.urn_draws_1
            self.participant.vars['urndraws2_b1'] = self.player.urn_draws_2
            self.participant.vars['urndraws3_b1'] = self.player.urn_draws_3
            
            self.participant.vars['option_1_b1'] = self.player.option_1
            self.participant.vars['option_2_b1'] = self.player.option_2
            self.participant.vars['option_3_b1'] = self.player.option_3
            
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

            self.participant.vars['payoff_1_b'] = self.player.payoff_1
            self.participant.vars['payoff_2_b'] = self.player.payoff_2
            self.participant.vars['payoff_3_b'] = self.player.payoff_3



        self.player.decision_b_page += 1


##same urns as A , but Bernoulli instead of safe
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

        if self.participant.vars['choice'] and not self.participant.vars['safe']:

            Urn_1 = ['0', '1', '2', '3', '4', '5', '6', '7']
            Urn_2 = ['-9', '-5', '-4', '-3', '35', '40', '50', '60']
            Urn_3 = ['-2', '8']

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
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40
                    elif k == '50':
                        data_counts[i][k] = v * 50
                    elif k == '60':
                        data_counts[i][k] = v * 60
                    elif k == '-9':
                        data_counts[i][k] = v * -9
                    elif k == '-5':
                        data_counts[i][k] = v * -5
                    elif k == '-4':
                        data_counts[i][k] = v * -4
                    elif k == '-3':
                        data_counts[i][k] = v * -3
                    elif k == '-2':
                        data_counts[i][k] = v * -2
                    elif k == '8':
                        data_counts[i][k] = v * 8


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

            if self.player.decision_c_page == 1:
                self.participant.vars['payoff_c1_1'] = self.player.payoff = payoffs
                self.participant.vars['urndraws1_c1_1'] = self.player.urn_draws_1
                self.participant.vars['urndraws2_c1_1'] = self.player.urn_draws_2
                self.participant.vars['urndraws3_c1_1'] = self.player.urn_draws_3
                self.participant.vars['option_1_c1_1'] = self.player.option_1
                self.participant.vars['option_2_c1_1'] = self.player.option_2
                self.participant.vars['option_3_c1_1'] = self.player.option_3

                self.participant.vars['payoff_1_c_1'] = self.player.payoff_1
                self.participant.vars['payoff_2_c_1'] = self.player.payoff_2
                self.participant.vars['payoff_3_c_1'] = self.player.payoff_3

                self.player.option_1 = 0
                self.player.option_2 = 0
                self.player.option_3 = 0

            if self.player.decision_c_page == 2:
                self.participant.vars['payoff_c1_2'] = self.player.payoff = payoffs
                self.participant.vars['urndraws1_c1_2'] = self.player.urn_draws_1
                self.participant.vars['urndraws2_c1_2'] = self.player.urn_draws_2
                self.participant.vars['urndraws3_c1_2'] = self.player.urn_draws_3
                self.participant.vars['option_1_c1_2'] = self.player.option_1
                self.participant.vars['option_2_c1_2'] = self.player.option_2
                self.participant.vars['option_3_c1_2'] = self.player.option_3

                self.participant.vars['payoff_1_c_2'] = self.player.payoff_1
                self.participant.vars['payoff_2_c_2'] = self.player.payoff_2
                self.participant.vars['payoff_3_c_2'] = self.player.payoff_3

                self.player.option_1 = 0
                self.player.option_2 = 0
                self.player.option_3 = 0

            if self.player.decision_c_page == 3:
                self.participant.vars['payoff_c1_3'] = self.player.payoff = payoffs
                self.participant.vars['urndraws1_c1_3'] = self.player.urn_draws_1
                self.participant.vars['urndraws2_c1_3'] = self.player.urn_draws_2
                self.participant.vars['urndraws3_c1_3'] = self.player.urn_draws_3
                self.participant.vars['option_1_c1_3'] = self.player.option_1
                self.participant.vars['option_2_c1_3'] = self.player.option_2
                self.participant.vars['option_3_c1_3'] = self.player.option_3

                self.participant.vars['payoff_1_c_3'] = self.player.payoff_1
                self.participant.vars['payoff_2_c_3'] = self.player.payoff_2
                self.participant.vars['payoff_3_c_3'] = self.player.payoff_3

                self.participant.vars['payoff_c1'] = self.participant.vars['payoff_c1_1'] + self.participant.vars[
                    'payoff_c1_2'] + self.participant.vars['payoff_c1_3']
                self.participant.vars['urndraws1_c1'] = self.participant.vars['urndraws1_c1_1'] + self.participant.vars[
                    'urndraws1_c1_2'] + self.participant.vars['urndraws1_c1_3']
                self.participant.vars['urndraws2_c1'] = self.participant.vars['urndraws2_c1_1'] + self.participant.vars[
                    'urndraws2_c1_2'] + self.participant.vars['urndraws2_c1_3']
                self.participant.vars['urndraws3_c1'] = self.participant.vars['urndraws3_c1_1'] + self.participant.vars[
                    'urndraws3_c1_2'] + self.participant.vars['urndraws3_c1_3']
                self.participant.vars['option_1_c1'] = self.participant.vars['option_1_c1_1'] + self.participant.vars[
                    'option_1_c1_2'] + self.participant.vars['option_1_c1_3']
                self.participant.vars['option_2_c1'] = self.participant.vars['option_2_c1_1'] + self.participant.vars['option_2_c1_2'] + self.participant.vars['option_2_c1_3']
                self.participant.vars['option_3_c1'] = self.participant.vars['option_3_c1_1'] + self.participant.vars['option_3_c1_2'] + self.participant.vars['option_3_c1_3']

                self.participant.vars['payoff_1_c'] = self.participant.vars['payoff_1_c_1'] + self.participant.vars['payoff_1_c_2'] + self.participant.vars['payoff_1_c_3']
                self.participant.vars['payoff_2_c'] = self.participant.vars['payoff_2_c_1'] + self.participant.vars['payoff_2_c_2'] + self.participant.vars['payoff_2_c_3']
                self.participant.vars['payoff_3_c'] = self.participant.vars['payoff_3_c_1'] + self.participant.vars['payoff_3_c_2'] + self.participant.vars['payoff_3_c_3']



        elif not self.participant.vars['choice'] and not self.participant.vars['safe'] :

            Urn_1 = ['0', '1', '2', '3', '4', '5', '6', '7']
            Urn_2 = ['-9', '-5', '-4', '-3', '35', '40', '50', '60']
            Urn_3 = ['-2', '8']

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
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40
                    elif k == '50':
                        data_counts[i][k] = v * 50
                    elif k == '60':
                        data_counts[i][k] = v * 60
                    elif k == '-9':
                        data_counts[i][k] = v * -9
                    elif k == '-5':
                        data_counts[i][k] = v * -5
                    elif k == '-4':
                        data_counts[i][k] = v * -4
                    elif k == '-3':
                        data_counts[i][k] = v * -3
                    elif k == '-2':
                        data_counts[i][k] = v * -2
                    elif k == '8':
                        data_counts[i][k] = v * 8

            self.player.payoff = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    self.player.payoff += values

            self.participant.vars['payoff_c1'] = self.player.payoff
            self.participant.vars['urndraws1_c1'] = self.player.urn_draws_1
            self.participant.vars['urndraws2_c1'] = self.player.urn_draws_2
            self.participant.vars['urndraws3_c1'] = self.player.urn_draws_3

            self.participant.vars['option_1_c1'] = self.player.option_1
            self.participant.vars['option_2_c1'] = self.player.option_2
            self.participant.vars['option_3_c1'] = self.player.option_3

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

            self.participant.vars['payoff_1_c'] = self.player.payoff_1
            self.participant.vars['payoff_2_c'] = self.player.payoff_2
            self.participant.vars['payoff_3_c'] = self.player.payoff_3

        self.player.decision_c_page += 1


##same urns as B, but Bernoulli instead of safe and higher mean of risk
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

               }

    def before_next_page(self):

        if self.participant.vars['choice'] and not self.participant.vars['safe'] :

            Urn_1 = ['0', '1', '2', '3', '4', '5', '6', '7']
            Urn_2 = ['-10', '-5', '-4', '-3', '35', '40', '50', '55']
            Urn_3 = ['-2', '8']

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
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40
                    elif k == '50':
                        data_counts[i][k] = v * 50
                    elif k == '55':
                        data_counts[i][k] = v * 55
                    elif k == '-10':
                        data_counts[i][k] = v * -10
                    elif k == '-5':
                        data_counts[i][k] = v * -5
                    elif k == '-4':
                        data_counts[i][k] = v * -4
                    elif k == '-3':
                        data_counts[i][k] = v * -3
                    elif k == '-2':
                        data_counts[i][k] = v * -2
                    elif k == '8':
                        data_counts[i][k] = v * 8

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

            if self.player.decision_d_page == 1:
                self.participant.vars['payoff_d1_1'] = self.player.payoff = payoffs
                self.participant.vars['urndraws1_d1_1'] = self.player.urn_draws_1
                self.participant.vars['urndraws2_d1_1'] = self.player.urn_draws_2
                self.participant.vars['urndraws3_d1_1'] = self.player.urn_draws_3
                self.participant.vars['option_1_d1_1'] = self.player.option_1
                self.participant.vars['option_2_d1_1'] = self.player.option_2
                self.participant.vars['option_3_d1_1'] = self.player.option_3

                self.participant.vars['payoff_1_d_1'] = self.player.payoff_1
                self.participant.vars['payoff_2_d_1'] = self.player.payoff_2
                self.participant.vars['payoff_3_d_1'] = self.player.payoff_3

                self.player.option_1 = 0
                self.player.option_2 = 0
                self.player.option_3 = 0

            if self.player.decision_d_page == 2:
                self.participant.vars['payoff_d1_2'] = self.player.payoff = payoffs
                self.participant.vars['urndraws1_d1_2'] = self.player.urn_draws_1
                self.participant.vars['urndraws2_d1_2'] = self.player.urn_draws_2
                self.participant.vars['urndraws3_d1_2'] = self.player.urn_draws_3
                self.participant.vars['option_1_d1_2'] = self.player.option_1
                self.participant.vars['option_2_d1_2'] = self.player.option_2
                self.participant.vars['option_3_d1_2'] = self.player.option_3

                self.participant.vars['payoff_1_d_2'] = self.player.payoff_1
                self.participant.vars['payoff_2_d_2'] = self.player.payoff_2
                self.participant.vars['payoff_3_d_2'] = self.player.payoff_3

                self.player.option_1 = 0
                self.player.option_2 = 0
                self.player.option_3 = 0

            if self.player.decision_d_page == 3:
                self.participant.vars['payoff_d1_3'] = self.player.payoff = payoffs
                self.participant.vars['urndraws1_d1_3'] = self.player.urn_draws_1
                self.participant.vars['urndraws2_d1_3'] = self.player.urn_draws_2
                self.participant.vars['urndraws3_d1_3'] = self.player.urn_draws_3
                self.participant.vars['option_1_d1_3'] = self.player.option_1
                self.participant.vars['option_2_d1_3'] = self.player.option_2
                self.participant.vars['option_3_d1_3'] = self.player.option_3

                self.participant.vars['payoff_1_d_3'] = self.player.payoff_1
                self.participant.vars['payoff_2_d_3'] = self.player.payoff_2
                self.participant.vars['payoff_3_d_3'] = self.player.payoff_3

                self.participant.vars['payoff_d1'] = self.participant.vars['payoff_d1_1'] + self.participant.vars[
                    'payoff_d1_2'] + self.participant.vars['payoff_d1_3']
                self.participant.vars['urndraws1_d1'] = self.participant.vars['urndraws1_d1_1'] + self.participant.vars[
                    'urndraws1_d1_2'] + self.participant.vars['urndraws1_d1_3']
                self.participant.vars['urndraws2_d1'] = self.participant.vars['urndraws2_d1_1'] + self.participant.vars[
                    'urndraws2_d1_2'] + self.participant.vars['urndraws2_d1_3']
                self.participant.vars['urndraws3_d1'] = self.participant.vars['urndraws3_d1_1'] + self.participant.vars[
                    'urndraws3_d1_2'] + self.participant.vars['urndraws3_d1_3']
                self.participant.vars['option_1_d1'] = self.participant.vars['option_1_d1_1'] + self.participant.vars[
                    'option_1_d1_2'] + self.participant.vars['option_1_d1_3']
                self.participant.vars['option_2_d1'] = self.participant.vars['option_2_d1_1'] + self.participant.vars['option_2_d1_2'] + self.participant.vars['option_2_d1_3']
                self.participant.vars['option_3_d1'] = self.participant.vars['option_3_d1_1'] + self.participant.vars['option_3_d1_2'] + self.participant.vars['option_3_d1_3']
                
                self.participant.vars['payoff_1_d'] = self.participant.vars['payoff_1_d_1'] + self.participant.vars['payoff_1_d_2'] + self.participant.vars['payoff_1_d_3']
                self.participant.vars['payoff_2_d'] = self.participant.vars['payoff_2_d_1'] + self.participant.vars['payoff_2_d_2'] + self.participant.vars['payoff_2_d_3']
                self.participant.vars['payoff_3_d'] = self.participant.vars['payoff_3_d_1'] + self.participant.vars['payoff_3_d_2'] + self.participant.vars['payoff_3_d_3']

        elif not self.participant.vars['choice'] and not self.participant.vars['safe'] :

            Urn_1 = ['0', '1', '2', '3', '4', '5', '6', '7']
            Urn_2 = ['-10', '-5', '-4', '-3', '35', '40', '50', '55']
            Urn_3 = ['-2', '8']

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
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40
                    elif k == '50':
                        data_counts[i][k] = v * 50
                    elif k == '55':
                        data_counts[i][k] = v * 55
                    elif k == '-10':
                        data_counts[i][k] = v * -10
                    elif k == '-5':
                        data_counts[i][k] = v * -5
                    elif k == '-4':
                        data_counts[i][k] = v * -4
                    elif k == '-3':
                        data_counts[i][k] = v * -3
                    elif k == '-2':
                        data_counts[i][k] = v * -2
                    elif k == '8':
                        data_counts[i][k] = v * 8

            self.player.payoff = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    self.player.payoff += values

            self.participant.vars['payoff_d1'] = self.player.payoff
            self.participant.vars['urndraws1_d1'] = self.player.urn_draws_1
            self.participant.vars['urndraws2_d1'] = self.player.urn_draws_2
            self.participant.vars['urndraws3_d1'] = self.player.urn_draws_3
            
            self.participant.vars['option_1_d1'] = self.player.option_1
            self.participant.vars['option_2_d1'] = self.player.option_2
            self.participant.vars['option_3_d1'] = self.player.option_3

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

            self.participant.vars['payoff_1_d'] = self.player.payoff_1
            self.participant.vars['payoff_2_d'] = self.player.payoff_2
            self.participant.vars['payoff_3_d'] = self.player.payoff_3

        self.player.decision_d_page += 1


##crazy differences and lower mean
class PriorsE(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == self.participant.vars['options']['E']

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

               }

    def before_next_page(self):

        if self.participant.vars['choice'] and not self.participant.vars['safe']:

            Urn_1 = ['0', '1', '2', '3', '4', '5', '6', '7']
            Urn_2 = ['-19', '-5', '-4', '-3', '35', '40', '50', '100']
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
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40
                    elif k == '50':
                        data_counts[i][k] = v * 50
                    elif k == '100':
                        data_counts[i][k] = v * 100
                    elif k == '-19':
                        data_counts[i][k] = v * -19
                    elif k == '-5':
                        data_counts[i][k] = v * -5
                    elif k == '-4':
                        data_counts[i][k] = v * -4
                    elif k == '-3':
                        data_counts[i][k] = v * -3


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

            if self.player.decision_e_page == 1:
                self.participant.vars['payoff_e1_1'] = self.player.payoff = payoffs
                self.participant.vars['urndraws1_e1_1'] = self.player.urn_draws_1
                self.participant.vars['urndraws2_e1_1'] = self.player.urn_draws_2
                self.participant.vars['urndraws3_e1_1'] = self.player.urn_draws_3
                self.participant.vars['option_1_e1_1'] = self.player.option_1
                self.participant.vars['option_2_e1_1'] = self.player.option_2
                self.participant.vars['option_3_e1_1'] = self.player.option_3

                self.participant.vars['payoff_1_e_1'] = self.player.payoff_1
                self.participant.vars['payoff_2_e_1'] = self.player.payoff_2
                self.participant.vars['payoff_3_e_1'] = self.player.payoff_3

                self.player.option_1 = 0
                self.player.option_2 = 0
                self.player.option_3 = 0

            if self.player.decision_e_page == 2:
                self.participant.vars['payoff_e1_2'] = self.player.payoff = payoffs
                self.participant.vars['urndraws1_e1_2'] = self.player.urn_draws_1
                self.participant.vars['urndraws2_e1_2'] = self.player.urn_draws_2
                self.participant.vars['urndraws3_e1_2'] = self.player.urn_draws_3
                self.participant.vars['option_1_e1_2'] = self.player.option_1
                self.participant.vars['option_2_e1_2'] = self.player.option_2
                self.participant.vars['option_3_e1_2'] = self.player.option_3

                self.participant.vars['payoff_1_e_2'] = self.player.payoff_1
                self.participant.vars['payoff_2_e_2'] = self.player.payoff_2
                self.participant.vars['payoff_3_e_2'] = self.player.payoff_3

                self.player.option_1 = 0
                self.player.option_2 = 0
                self.player.option_3 = 0

            if self.player.decision_e_page == 3:
                self.participant.vars['payoff_e1_3'] = self.player.payoff = payoffs
                self.participant.vars['urndraws1_e1_3'] = self.player.urn_draws_1
                self.participant.vars['urndraws2_e1_3'] = self.player.urn_draws_2
                self.participant.vars['urndraws3_e1_3'] = self.player.urn_draws_3
                self.participant.vars['option_1_e1_3'] = self.player.option_1
                self.participant.vars['option_2_e1_3'] = self.player.option_2
                self.participant.vars['option_3_e1_3'] = self.player.option_3

                self.participant.vars['payoff_1_e_3'] = self.player.payoff_1
                self.participant.vars['payoff_2_e_3'] = self.player.payoff_2
                self.participant.vars['payoff_3_e_3'] = self.player.payoff_3

                self.participant.vars['payoff_e1'] = self.participant.vars['payoff_e1_1'] + self.participant.vars[
                    'payoff_e1_2'] + self.participant.vars['payoff_e1_3']
                self.participant.vars['urndraws1_e1'] = self.participant.vars['urndraws1_e1_1'] + self.participant.vars[
                    'urndraws1_e1_2'] + self.participant.vars['urndraws1_e1_3']
                self.participant.vars['urndraws2_e1'] = self.participant.vars['urndraws2_e1_1'] + self.participant.vars[
                    'urndraws2_e1_2'] + self.participant.vars['urndraws2_e1_3']
                self.participant.vars['urndraws3_e1'] = self.participant.vars['urndraws3_e1_1'] + self.participant.vars[
                    'urndraws3_e1_2'] + self.participant.vars['urndraws3_e1_3']
                self.participant.vars['option_1_e1'] = self.participant.vars['option_1_e1_1'] + self.participant.vars[
                    'option_1_e1_2'] + self.participant.vars['option_1_e1_3']
                self.participant.vars['option_2_e1'] = self.participant.vars['option_2_e1_1'] + self.participant.vars['option_2_e1_2'] + self.participant.vars['option_2_e1_3']
                self.participant.vars['option_3_e1'] = self.participant.vars['option_3_e1_1'] + self.participant.vars['option_3_e1_2'] + self.participant.vars['option_3_e1_3']

                self.participant.vars['payoff_1_e'] = self.participant.vars['payoff_1_e_1'] + self.participant.vars['payoff_1_e_2'] + self.participant.vars['payoff_1_e_3']
                self.participant.vars['payoff_2_e'] = self.participant.vars['payoff_2_e_1'] + self.participant.vars['payoff_2_e_2'] + self.participant.vars['payoff_2_e_3']
                self.participant.vars['payoff_3_e'] = self.participant.vars['payoff_3_e_1'] + self.participant.vars['payoff_3_e_2'] + self.participant.vars['payoff_3_e_3']

        elif not self.participant.vars['choice'] and not self.participant.vars['safe']:

            Urn_1 = ['0', '1', '2', '3', '4', '5', '6', '7']
            Urn_2 = ['-19', '-5', '-4', '-3', '35', '40', '50', '100']
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
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40
                    elif k == '50':
                        data_counts[i][k] = v * 50
                    elif k == '100':
                        data_counts[i][k] = v * 100
                    elif k == '-19':
                        data_counts[i][k] = v * -19
                    elif k == '-5':
                        data_counts[i][k] = v * -5
                    elif k == '-4':
                        data_counts[i][k] = v * -4
                    elif k == '-3':
                        data_counts[i][k] = v * -3

            self.player.payoff = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    self.player.payoff += values

            self.participant.vars['payoff_e1'] = self.player.payoff
            self.participant.vars['urndraws1_e1'] = self.player.urn_draws_1
            self.participant.vars['urndraws2_e1'] = self.player.urn_draws_2
            self.participant.vars['urndraws3_e1'] = self.player.urn_draws_3
            
            self.participant.vars['option_1_e1'] = self.player.option_1
            self.participant.vars['option_2_e1'] = self.player.option_2
            self.participant.vars['option_3_e1'] = self.player.option_3

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

            self.participant.vars['payoff_1_e'] = self.player.payoff_1
            self.participant.vars['payoff_2_e'] = self.player.payoff_2
            self.participant.vars['payoff_3_e'] = self.player.payoff_3

        self.player.decision_e_page += 1


##crazy differences and higher mean

class PriorsF(Page):
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

               }

    def before_next_page(self):

        if self.participant.vars['choice'] and not self.participant.vars['safe']:

            Urn_1 = ['0', '1', '2', '3', '4', '5', '6', '7']
            Urn_2 = ['-20', '-5', '-4', '-3', '35', '40', '50', '95']
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
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40
                    elif k == '50':
                        data_counts[i][k] = v * 50
                    elif k == '95':
                        data_counts[i][k] = v * 95
                    elif k == '-20':
                        data_counts[i][k] = v * -20
                    elif k == '-5':
                        data_counts[i][k] = v * -5
                    elif k == '-4':
                        data_counts[i][k] = v * -4
                    elif k == '-3':
                        data_counts[i][k] = v * -3

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

            if self.player.decision_f_page == 1:
                self.participant.vars['payoff_f1_1'] = self.player.payoff = payoffs
                self.participant.vars['urndraws1_f1_1'] = self.player.urn_draws_1
                self.participant.vars['urndraws2_f1_1'] = self.player.urn_draws_2
                self.participant.vars['urndraws3_f1_1'] = self.player.urn_draws_3
                self.participant.vars['option_1_f1_1'] = self.player.option_1
                self.participant.vars['option_2_f1_1'] = self.player.option_2
                self.participant.vars['option_3_f1_1'] = self.player.option_3

                self.participant.vars['payoff_1_f_1'] = self.player.payoff_1
                self.participant.vars['payoff_2_f_1'] = self.player.payoff_2
                self.participant.vars['payoff_3_f_1'] = self.player.payoff_3

                self.player.option_1 = 0
                self.player.option_2 = 0
                self.player.option_3 = 0

            if self.player.decision_f_page == 2:
                self.participant.vars['payoff_f1_2'] = self.player.payoff = payoffs
                self.participant.vars['urndraws1_f1_2'] = self.player.urn_draws_1
                self.participant.vars['urndraws2_f1_2'] = self.player.urn_draws_2
                self.participant.vars['urndraws3_f1_2'] = self.player.urn_draws_3
                self.participant.vars['option_1_f1_2'] = self.player.option_1
                self.participant.vars['option_2_f1_2'] = self.player.option_2
                self.participant.vars['option_3_f1_2'] = self.player.option_3

                self.participant.vars['payoff_1_f_2'] = self.player.payoff_1
                self.participant.vars['payoff_2_f_2'] = self.player.payoff_2
                self.participant.vars['payoff_3_f_2'] = self.player.payoff_3

                self.player.option_1 = 0
                self.player.option_2 = 0
                self.player.option_3 = 0

            if self.player.decision_f_page == 3:
                self.participant.vars['payoff_f1_3'] = self.player.payoff = payoffs
                self.participant.vars['urndraws1_f1_3'] = self.player.urn_draws_1
                self.participant.vars['urndraws2_f1_3'] = self.player.urn_draws_2
                self.participant.vars['urndraws3_f1_3'] = self.player.urn_draws_3
                self.participant.vars['option_1_f1_3'] = self.player.option_1
                self.participant.vars['option_2_f1_3'] = self.player.option_2
                self.participant.vars['option_3_f1_3'] = self.player.option_3

                self.participant.vars['payoff_1_f_3'] = self.player.payoff_1
                self.participant.vars['payoff_2_f_3'] = self.player.payoff_2
                self.participant.vars['payoff_3_f_3'] = self.player.payoff_3

                self.participant.vars['payoff_f1'] = self.participant.vars['payoff_f1_1'] + self.participant.vars[
                    'payoff_f1_2'] + self.participant.vars['payoff_f1_3']
                self.participant.vars['urndraws1_f1'] = self.participant.vars['urndraws1_f1_1'] + self.participant.vars[
                    'urndraws1_f1_2'] + self.participant.vars['urndraws1_f1_3']
                self.participant.vars['urndraws2_f1'] = self.participant.vars['urndraws2_f1_1'] + self.participant.vars[
                    'urndraws2_f1_2'] + self.participant.vars['urndraws2_f1_3']
                self.participant.vars['urndraws3_f1'] = self.participant.vars['urndraws3_f1_1'] + self.participant.vars[
                    'urndraws3_f1_2'] + self.participant.vars['urndraws3_f1_3']
                self.participant.vars['option_1_f1'] = self.participant.vars['option_1_f1_1'] + self.participant.vars[
                    'option_1_f1_2'] + self.participant.vars['option_1_f1_3']
                self.participant.vars['option_2_f1'] = self.participant.vars['option_2_f1_1'] + self.participant.vars['option_2_f1_2'] + self.participant.vars['option_2_f1_3']
                self.participant.vars['option_3_f1'] = self.participant.vars['option_3_f1_1'] + self.participant.vars['option_3_f1_2'] + self.participant.vars['option_3_f1_3']

                self.participant.vars['payoff_1_f'] = self.participant.vars['payoff_1_f_1'] + self.participant.vars['payoff_1_f_2'] + self.participant.vars['payoff_1_f_3']
                self.participant.vars['payoff_2_f'] = self.participant.vars['payoff_2_f_1'] + self.participant.vars['payoff_2_f_2'] + self.participant.vars['payoff_2_f_3']
                self.participant.vars['payoff_3_f'] = self.participant.vars['payoff_3_f_1'] + self.participant.vars['payoff_3_f_2'] + self.participant.vars['payoff_3_f_3']

        elif not self.participant.vars['choice'] and not self.participant.vars['safe']:

            Urn_1 = ['0', '1', '2', '3', '4', '5', '6', '7']
            Urn_2 = ['-20', '-5', '-4', '-3', '35', '40', '50', '95']
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
                    elif k == '35':
                        data_counts[i][k] = v * 35
                    elif k == '40':
                        data_counts[i][k] = v * 40
                    elif k == '50':
                        data_counts[i][k] = v * 50
                    elif k == '95':
                        data_counts[i][k] = v * 95
                    elif k == '-20':
                        data_counts[i][k] = v * -20
                    elif k == '-5':
                        data_counts[i][k] = v * -5
                    elif k == '-4':
                        data_counts[i][k] = v * -4
                    elif k == '-3':
                        data_counts[i][k] = v * -3

            self.player.payoff = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    self.player.payoff += values

            self.participant.vars['payoff_f1'] = self.player.payoff
            self.participant.vars['urndraws1_f1'] = self.player.urn_draws_1
            self.participant.vars['urndraws2_f1'] = self.player.urn_draws_2
            self.participant.vars['urndraws3_f1'] = self.player.urn_draws_3
            
            self.participant.vars['option_1_f1'] = self.player.option_1
            self.participant.vars['option_2_f1'] = self.player.option_2
            self.participant.vars['option_3_f1'] = self.player.option_3
            
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

            self.participant.vars['payoff_1_f'] = self.player.payoff_1
            self.participant.vars['payoff_2_f'] = self.player.payoff_2
            self.participant.vars['payoff_3_f'] = self.player.payoff_3

        self.player.decision_f_page += 1


##only positives? But still big eyes?

class PriorsG(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == self.participant.vars['options']['G']

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'draw': self.participant.vars['draw'],
               'sampling': self.participant.vars['sampling'],

               }

class DecisionG1(Page):
    form_model = 'player'

    def is_displayed(self):
        if not self.participant.vars['sampling'] and not self.participant.vars['choice'] and self.player.decision_g_page == 1:
            return self.round_number == self.participant.vars['options']['G']
        elif not self.participant.vars['sampling'] and self.participant.vars['choice'] and self.player.decision_g_page <= 3:
            return self.round_number == self.participant.vars['options']['G']


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

        if self.participant.vars['choice'] and not self.participant.vars['safe']:

            Urn_1 = ['2', '3', '4', '5', '6', '7', '8', '9']
            Urn_2 = ['0', '100']
            Urn_3 = ['1', '10']

            weights_1 = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
            weights_2 = [0.5, 0.5]
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
                    if k == '2':
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
                    elif k == '0':
                        data_counts[i][k] = v * 0
                    elif k == '100':
                        data_counts[i][k] = v * 100
                    elif k == '10':
                        data_counts[i][k] = v * 10
                    elif k == '1':
                        data_counts[i][k] = v * 1


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

            if self.player.decision_g_page == 1:
                self.participant.vars['payoff_g1_1'] = self.player.payoff = payoffs
                self.participant.vars['urndraws1_g1_1'] = self.player.urn_draws_1
                self.participant.vars['urndraws2_g1_1'] = self.player.urn_draws_2
                self.participant.vars['urndraws3_g1_1'] = self.player.urn_draws_3
                self.participant.vars['option_1_g1_1'] = self.player.option_1
                self.participant.vars['option_2_g1_1'] = self.player.option_2
                self.participant.vars['option_3_g1_1'] = self.player.option_3

                self.participant.vars['payoff_1_g_1'] = self.player.payoff_1
                self.participant.vars['payoff_2_g_1'] = self.player.payoff_2
                self.participant.vars['payoff_3_g_1'] = self.player.payoff_3

                self.player.option_1 = 0
                self.player.option_2 = 0
                self.player.option_3 = 0

            if self.player.decision_g_page == 2:
                self.participant.vars['payoff_g1_2'] = self.player.payoff = payoffs
                self.participant.vars['urndraws1_g1_2'] = self.player.urn_draws_1
                self.participant.vars['urndraws2_g1_2'] = self.player.urn_draws_2
                self.participant.vars['urndraws3_g1_2'] = self.player.urn_draws_3
                self.participant.vars['option_1_g1_2'] = self.player.option_1
                self.participant.vars['option_2_g1_2'] = self.player.option_2
                self.participant.vars['option_3_g1_2'] = self.player.option_3

                self.participant.vars['payoff_1_g_2'] = self.player.payoff_1
                self.participant.vars['payoff_2_g_2'] = self.player.payoff_2
                self.participant.vars['payoff_3_g_2'] = self.player.payoff_3

                self.player.option_1 = 0
                self.player.option_2 = 0
                self.player.option_3 = 0

            if self.player.decision_g_page == 3:
                self.participant.vars['payoff_g1_3'] = self.player.payoff = payoffs
                self.participant.vars['urndraws1_g1_3'] = self.player.urn_draws_1
                self.participant.vars['urndraws2_g1_3'] = self.player.urn_draws_2
                self.participant.vars['urndraws3_g1_3'] = self.player.urn_draws_3
                self.participant.vars['option_1_g1_3'] = self.player.option_1
                self.participant.vars['option_2_g1_3'] = self.player.option_2
                self.participant.vars['option_3_g1_3'] = self.player.option_3

                self.participant.vars['payoff_1_g_3'] = self.player.payoff_1
                self.participant.vars['payoff_2_g_3'] = self.player.payoff_2
                self.participant.vars['payoff_3_g_3'] = self.player.payoff_3

                self.participant.vars['payoff_g1'] = self.participant.vars['payoff_g1_1'] + self.participant.vars['payoff_g1_2'] + self.participant.vars['payoff_g1_3']
                self.participant.vars['urndraws1_g1'] = self.participant.vars['urndraws1_g1_1'] + self.participant.vars['urndraws1_g1_2'] + self.participant.vars['urndraws1_g1_3']
                self.participant.vars['urndraws2_g1'] = self.participant.vars['urndraws2_g1_1'] + self.participant.vars['urndraws2_g1_2'] + self.participant.vars['urndraws2_g1_3']
                self.participant.vars['urndraws3_g1'] = self.participant.vars['urndraws3_g1_1'] + self.participant.vars['urndraws3_g1_2'] + self.participant.vars['urndraws3_g1_3']
                self.participant.vars['option_1_g1'] = self.participant.vars['option_1_g1_1'] + self.participant.vars['option_1_g1_2'] + self.participant.vars['option_1_g1_3']
                self.participant.vars['option_2_g1'] = self.participant.vars['option_2_g1_1'] + self.participant.vars['option_2_g1_2'] + self.participant.vars['option_2_g1_3']
                self.participant.vars['option_3_g1'] = self.participant.vars['option_3_g1_1'] + self.participant.vars['option_3_g1_2'] + self.participant.vars['option_3_g1_3']

                self.participant.vars['payoff_1_g'] = self.participant.vars['payoff_1_g_1'] + self.participant.vars['payoff_1_g_2'] + self.participant.vars['payoff_1_g_3']
                self.participant.vars['payoff_2_g'] = self.participant.vars['payoff_2_g_1'] + self.participant.vars['payoff_2_g_2'] + self.participant.vars['payoff_2_g_3']
                self.participant.vars['payoff_3_g'] = self.participant.vars['payoff_3_g_1'] + self.participant.vars['payoff_3_g_2'] + self.participant.vars['payoff_3_g_3']

        elif not self.participant.vars['choice'] and not self.participant.vars['safe']:

            Urn_1 = ['2', '3', '4', '5', '6', '7', '8', '9']
            Urn_2 = ['0', '100']
            Urn_3 = ['1', '10']

            weights_1 = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
            weights_2 = [0.5, 0.5]
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
                    if k == '2':
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
                    elif k == '0':
                        data_counts[i][k] = v * 0
                    elif k == '100':
                        data_counts[i][k] = v * 100
                    elif k == '10':
                        data_counts[i][k] = v * 10
                    elif k == '1':
                        data_counts[i][k] = v * 1

            self.player.payoff = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    self.player.payoff += values

            self.participant.vars['payoff_g1'] = self.player.payoff
            self.participant.vars['urndraws1_g1'] = self.player.urn_draws_1
            self.participant.vars['urndraws2_g1'] = self.player.urn_draws_2
            self.participant.vars['urndraws3_g1'] = self.player.urn_draws_3
            
            self.participant.vars['option_1_g1'] = self.player.option_1
            self.participant.vars['option_2_g1'] = self.player.option_2
            self.participant.vars['option_3_g1'] = self.player.option_3            

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

            self.participant.vars['payoff_1_g'] = self.player.payoff_1
            self.participant.vars['payoff_2_g'] = self.player.payoff_2
            self.participant.vars['payoff_3_g'] = self.player.payoff_3

        self.player.decision_g_page += 1


class Feedback(Page):
    form_model = 'player'

    def is_displayed(self):
        if self.participant.vars['choice'] and self.participant.vars['sampling']:
            return self.round_number <= Constants.num_rounds_choice
        elif not self.participant.vars['choice'] and self.participant.vars['sampling']:
            return self.round_number <= Constants.num_rounds_points
        else:
            pass


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
        if self.player.questionnaire_page == 6:
            stages = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
            stage_payment = random.choice(stages)
            self.player.stage_payment = stage_payment
            #self.player.stages = stages

            self.player.payoff_a = self.participant.vars['payoff_a1']
            self.player.payoff_b = self.participant.vars['payoff_b1']
            self.player.payoff_c = self.participant.vars['payoff_c1']
            self.player.payoff_d = self.participant.vars['payoff_d1']
            self.player.payoff_e = self.participant.vars['payoff_e1']
            self.player.payoff_f = self.participant.vars['payoff_f1']
            self.player.payoff_g = self.participant.vars['payoff_g1']

            self.player.urn_draws_1_a = self.participant.vars['urndraws1_a1']
            self.player.urn_draws_1_b = self.participant.vars['urndraws1_b1']
            self.player.urn_draws_1_c = self.participant.vars['urndraws1_c1']
            self.player.urn_draws_1_d = self.participant.vars['urndraws1_d1']
            self.player.urn_draws_1_e = self.participant.vars['urndraws1_e1']
            self.player.urn_draws_1_f = self.participant.vars['urndraws1_f1']
            self.player.urn_draws_1_g = self.participant.vars['urndraws1_g1']

            self.player.urn_draws_2_a = self.participant.vars['urndraws2_a1']
            self.player.urn_draws_2_b = self.participant.vars['urndraws2_b1']
            self.player.urn_draws_2_c = self.participant.vars['urndraws2_c1']
            self.player.urn_draws_2_d = self.participant.vars['urndraws2_d1']
            self.player.urn_draws_2_e = self.participant.vars['urndraws2_e1']
            self.player.urn_draws_2_f = self.participant.vars['urndraws2_f1']
            self.player.urn_draws_2_g = self.participant.vars['urndraws2_g1']

            self.player.urn_draws_3_a = self.participant.vars['urndraws3_a1']
            self.player.urn_draws_3_b = self.participant.vars['urndraws3_b1']
            self.player.urn_draws_3_c = self.participant.vars['urndraws3_c1']
            self.player.urn_draws_3_d = self.participant.vars['urndraws3_d1']
            self.player.urn_draws_3_e = self.participant.vars['urndraws3_e1']
            self.player.urn_draws_3_f = self.participant.vars['urndraws3_f1']
            self.player.urn_draws_3_g = self.participant.vars['urndraws3_g1']
            
            self.player.option_1_a = self.participant.vars['option_1_a1']
            self.player.option_1_b = self.participant.vars['option_1_b1']
            self.player.option_1_c = self.participant.vars['option_1_c1']
            self.player.option_1_d = self.participant.vars['option_1_d1']
            self.player.option_1_e = self.participant.vars['option_1_e1']
            self.player.option_1_f = self.participant.vars['option_1_f1']
            self.player.option_1_g = self.participant.vars['option_1_g1']

            self.player.option_2_a = self.participant.vars['option_2_a1']
            self.player.option_2_b = self.participant.vars['option_2_b1']
            self.player.option_2_c = self.participant.vars['option_2_c1']
            self.player.option_2_d = self.participant.vars['option_2_d1']
            self.player.option_2_e = self.participant.vars['option_2_e1']
            self.player.option_2_f = self.participant.vars['option_2_f1']
            self.player.option_2_g = self.participant.vars['option_2_g1']

            self.player.option_3_a = self.participant.vars['option_3_a1']
            self.player.option_3_b = self.participant.vars['option_3_b1']
            self.player.option_3_c = self.participant.vars['option_3_c1']
            self.player.option_3_d = self.participant.vars['option_3_d1']
            self.player.option_3_e = self.participant.vars['option_3_e1']
            self.player.option_3_f = self.participant.vars['option_3_f1']
            self.player.option_3_g = self.participant.vars['option_3_g1']

            self.player.payoff_1_a = self.participant.vars['payoff_1_a']
            self.player.payoff_1_b = self.participant.vars['payoff_1_b']
            self.player.payoff_1_c = self.participant.vars['payoff_1_c']
            self.player.payoff_1_d = self.participant.vars['payoff_1_d']
            self.player.payoff_1_e = self.participant.vars['payoff_1_e']
            self.player.payoff_1_f = self.participant.vars['payoff_1_f']
            self.player.payoff_1_g = self.participant.vars['payoff_1_g']

            self.player.payoff_2_a = self.participant.vars['payoff_2_a']
            self.player.payoff_2_b = self.participant.vars['payoff_2_b']
            self.player.payoff_2_c = self.participant.vars['payoff_2_c']
            self.player.payoff_2_d = self.participant.vars['payoff_2_d']
            self.player.payoff_2_e = self.participant.vars['payoff_2_e']
            self.player.payoff_2_f = self.participant.vars['payoff_2_f']
            self.player.payoff_2_g = self.participant.vars['payoff_2_g']

            self.player.payoff_3_a = self.participant.vars['payoff_3_a']
            self.player.payoff_3_b = self.participant.vars['payoff_3_b']
            self.player.payoff_3_c = self.participant.vars['payoff_3_c']
            self.player.payoff_3_d = self.participant.vars['payoff_3_d']
            self.player.payoff_3_e = self.participant.vars['payoff_3_e']
            self.player.payoff_3_f = self.participant.vars['payoff_3_f']
            self.player.payoff_3_g = self.participant.vars['payoff_3_g']


class Disclose_Payoff(Page):
    form_model ='player'

    def is_displayed(self):
        if self.participant.vars['choice']:
            return self.round_number == Constants.num_rounds_choice
        else:
            return self.round_number == Constants.num_rounds_points

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'stage_payment': self.player.stage_payment,
               'urn_draws_1_a': self.player.urn_draws_1_a,
               'urn_draws_2_a': self.player.urn_draws_2_a,
               'urn_draws_3_a': self.player.urn_draws_3_a,
               'urn_draws_1_b': self.player.urn_draws_1_b,
               'urn_draws_2_b': self.player.urn_draws_2_b,
               'urn_draws_3_b': self.player.urn_draws_3_b,
               'urn_draws_1_c': self.player.urn_draws_1_c,
               'urn_draws_2_c': self.player.urn_draws_2_c,
               'urn_draws_3_c': self.player.urn_draws_3_c,
               'urn_draws_1_d': self.player.urn_draws_1_d,
               'urn_draws_2_d': self.player.urn_draws_2_d,
               'urn_draws_3_d': self.player.urn_draws_3_d,
               'urn_draws_1_e': self.player.urn_draws_1_e,
               'urn_draws_2_e': self.player.urn_draws_2_e,
               'urn_draws_3_e': self.player.urn_draws_3_e,
               'urn_draws_1_f': self.player.urn_draws_1_f,
               'urn_draws_2_f': self.player.urn_draws_2_f,
               'urn_draws_3_f': self.player.urn_draws_3_f,
               'urn_draws_1_g': self.player.urn_draws_1_g,
               'urn_draws_2_g': self.player.urn_draws_2_g,
               'urn_draws_3_g': self.player.urn_draws_3_g,
               'payoff_a': self.player.payoff_a,
               'payoff_b': self.player.payoff_b,
               'payoff_c': self.player.payoff_c,
               'payoff_d': self.player.payoff_d,
               'payoff_e': self.player.payoff_e,
               'payoff_f': self.player.payoff_f,
               'payoff_g': self.player.payoff_g,
               'option_1_a': self.player.option_1_a,
               'option_1_b': self.player.option_1_b,
               'option_1_c': self.player.option_1_c,
               'option_1_d': self.player.option_1_d,
               'option_1_e': self.player.option_1_e,
               'option_1_f': self.player.option_1_f,
               'option_1_g': self.player.option_1_g,
               'option_2_a': self.player.option_2_a,
               'option_2_b': self.player.option_2_b,
               'option_2_c': self.player.option_2_c,
               'option_2_d': self.player.option_2_d,
               'option_2_e': self.player.option_2_e,
               'option_2_f': self.player.option_2_f,
               'option_2_g': self.player.option_2_g,
               'option_3_a': self.player.option_3_a,
               'option_3_b': self.player.option_3_b,
               'option_3_c': self.player.option_3_c,
               'option_3_d': self.player.option_3_d,
               'option_3_e': self.player.option_3_e,
               'option_3_f': self.player.option_3_f,
               'option_3_g': self.player.option_3_g,
               'draw': self.participant.vars['draw'],
               'payoff_1_a': self.player.payoff_1_a,
               'payoff_1_b': self.player.payoff_1_b,
               'payoff_1_c': self.player.payoff_1_c,
               'payoff_1_d': self.player.payoff_1_d,
               'payoff_1_e': self.player.payoff_1_e,
               'payoff_1_f': self.player.payoff_1_f,
               'payoff_1_g': self.player.payoff_1_g,
               'payoff_2_a': self.player.payoff_2_a,
               'payoff_2_b': self.player.payoff_2_b,
               'payoff_2_c': self.player.payoff_2_c,
               'payoff_2_d': self.player.payoff_2_d,
               'payoff_2_e': self.player.payoff_2_e,
               'payoff_2_f': self.player.payoff_2_f,
               'payoff_2_g': self.player.payoff_2_g,
               'payoff_3_a': self.player.payoff_3_a,
               'payoff_3_b': self.player.payoff_3_b,
               'payoff_3_c': self.player.payoff_3_c,
               'payoff_3_d': self.player.payoff_3_d,
               'payoff_3_e': self.player.payoff_3_e,
               'payoff_3_f': self.player.payoff_3_f,
               'payoff_3_g': self.player.payoff_3_g,
               }

    def before_next_page(self):
        if self.player.stage_payment == "A":
            self.participant.payoff = self.player.payoff_a + 10
        elif self.player.stage_payment == "B":
            self.participant.payoff = self.player.payoff_b + 10
        elif self.player.stage_payment == "C":
            self.participant.payoff = self.player.payoff_c + 10
        elif self.player.stage_payment == "D":
            self.participant.payoff = self.player.payoff_d + 10
        elif self.player.stage_payment == "E":
            self.participant.payoff = self.player.payoff_e + 10
        elif self.player.stage_payment == "F":
            self.participant.payoff = self.player.payoff_f + 10
        elif self.player.stage_payment == "G":
            self.participant.payoff = self.player.payoff_g + 10


class FinalInfo(Page):
    def is_displayed(self):
        if self.participant.vars['choice']:
            return self.round_number == Constants.num_rounds_choice
        else:
            return self.round_number == Constants.num_rounds_points

    def vars_for_template(self):
        return {'participation_fee': self.session.config['participation_fee'],
                'total_payoff': self.participant.payoff_plus_participation_fee(),
                'bonus': self.participant.payoff.to_real_world_currency(self.session),
                'completion_code': self.participant.vars['completion_code'],
                }


page_sequence = [
    #DecisionTransition,
    PriorsA,
    DecisionA1,
    DecisionA1,
    DecisionA1,
    PriorsB,
    DecisionB1,
    DecisionB1,
    DecisionB1,
    PriorsC,
    DecisionC1,
    DecisionC1,
    DecisionC1,
    PriorsD,
    DecisionD1,
    DecisionD1,
    DecisionD1,
    PriorsE,
    DecisionE1,
    DecisionE1,
    DecisionE1,
    PriorsF,
    DecisionF1,
    DecisionF1,
    DecisionF1,
    PriorsG,
    DecisionG1,
    DecisionG1,
    DecisionG1,
    #Feedback,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    Disclose_Payoff,
    FinalInfo,
]
