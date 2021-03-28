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
from decimal import Decimal, ROUND_HALF_UP



########################################################################################################################
# Device ###############################################################################################################
########################################################################################################################

class Device(Page):
    def is_displayed(self):
        return self.round_number == 1

    form_model = 'player'
    form_fields = ['access_device']

    def before_next_page(self):

        if self.session.config['name'] == 'MS3':
            letters_and_digits = string.ascii_letters + string.digits
            result_str = ''.join((random.choice(letters_and_digits) for i in range(7))) + str(random.randint(1, 8))
            self.player.completion_code = result_str
            self.participant.vars['completion_code'] = result_str
            self.player.safe = self.participant.vars['safe'] = self.session.config['safe']
            self.player.sampling = self.participant.vars['sampling'] = self.session.config['sampling']
            self.player.incentive = self.participant.vars['incentive'] = self.session.config['incentive']

            treatments = ['choice', 'no_choice']
            weights_3 = [0.5, 0.5]
            draw_3 = choice(treatments, 1, p=weights_3)
            self.participant.vars['draw_3'] = draw_3[0]
            if draw_3[0] == 'choice':
                self.player.feedback_3 = self.participant.vars['feedback_3'] = False
                self.player.choice = self.participant.vars['choice'] = True
            else:
                self.player.feedback_3 = self.participant.vars['feedback_3'] = False
                self.player.choice = self.participant.vars['choice'] = False

            if self.participant.vars['safe']:
                order =['TSRH', 'STRH', 'RTSH', 'TRSH', 'SRTH', 'RSTH', 'HSTR', 'SHTR', 'THSR', 'HTSR', 'STHR', 'TSHR', 'TRHS',
                    'RTHS', 'HTRS', 'THRS', 'RHTS', 'HRTS', 'HRST', 'RHST', 'SHRT', 'HSRT', 'RSHT', 'SRHT']
                weights = [1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24,
                    1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24, 1/24]
                draw = choice(order, 1, p=weights)
                self.participant.vars['draw'] = draw[0]

            else:
                order = ['TSR', 'STR', 'RTS', 'TRS', 'SRT', 'RST']
                weights = [1/6, 1/6, 1/6, 1/6, 1/6, 1/6]
                draw = choice(order, 1, p=weights)
                self.participant.vars['draw'] = draw[0]


########################################################################################################################
# AttentionCheck ##########################################################################################################
########################################################################################################################

class AttentionCheck(Page):
    def is_displayed(self):
        return self.player.access_device != 0 and self.round_number == 1

    form_model = 'player'
    form_fields = ['attention_check_1', 'attention_check_2']

    def vars_for_template(self):
        return{
            'choice': self.participant.vars['choice']
        }


########################################################################################################################
# DeadEnd ##############################################################################################################
########################################################################################################################


class DeadEnd(Page):

    # this page is only displayed to people with mobile devices
    # which we do not want to partake and that are "trapped" on this page due to the missing {% next_button %}
    def is_displayed(self):
        return self.player.access_device == 0 or self.player.attention_check_1 == 0 or self.player.attention_check_2 != "chair" and self.round_number == 1


########################################################################################################################
# InstruStart ##########################################################################################################
########################################################################################################################


class InstruStart(Page):

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {'participation_fee': self.session.config['participation_fee'],
                'conversion_factor': int(self.session.config['real_world_currency_per_point'] * 100),
                'choice': self.participant.vars['choice'],
                'safe': self.participant.vars['safe'],
                'endowment_choice': Constants.endowment_choice,
                'endowment_points': Constants.endowment_points,
                'draw': self.participant.vars['draw'],
                'feedback_3': self.participant.vars['feedback_3'],

                }

    def before_next_page(self):
        self.player.instru_page += 1


########################################################################################################################
# ComprehensionQuestions ###############################################################################################
########################################################################################################################

class ComprehensionQuestions(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1 and self.player.controls != 1

    def vars_for_template(self):
        return {'participation_fee': self.session.config['participation_fee'],
                'conversion_factor': int(self.session.config['real_world_currency_per_point'] * 1000),
                'choice': self.participant.vars['choice'],
                'safe': self.participant.vars['safe'],
                'endowment_choice': Constants.endowment_choice,
                'endowment_points': Constants.endowment_points,
                }

    def get_form_fields(self):
        if self.participant.vars['choice'] :
            return ['cq1_MS3', 'cq2_MS3', 'cq3_MS3','cq4_MS3','cq5_MS3']
        elif not self.participant.vars['choice']:
            return ['cq1_MS3', 'cq2_MS3', 'cq3_MS3', 'cq4_MS3', 'cq5_MS3']

    def before_next_page(self):
        if self.participant.vars['choice']:
            if sum([self.player.cq1_MS3, self.player.cq2_MS3, self.player.cq3_MS3, self.player.cq4_MS3, self.player.cq5_MS3]) < 6:
                self.player.controls = 1
        else:
            if sum([self.player.cq1_MS3, self.player.cq2_MS3, self.player.cq3_MS3, self.player.cq4_MS3, self.player.cq5_MS3]) < 6:
                self.player.controls = 1

        self.player.comprehension_page += 1


class DeadEnd2(Page):
    def is_displayed(self) -> bool:
        return self.player.in_round(1).controls !=1 and self.round_number == 1



########################################################################################################################
# PRIORS ###############################################################################################################
########################################################################################################################

class PriorsTransition(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               }


class Priors(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'draw': self.participant.vars['draw'],
               'sampling': self.participant.vars['sampling'],

               }



########################################################################################################################
# DECISION 1 ###########################################################################################################
########################################################################################################################

class Decision(Page):
    form_model = 'player'

    def is_displayed(self):
        if not self.participant.vars['choice'] and self.player.decision_1_page == 1:
            return self.round_number == 1
        elif self.participant.vars['choice'] and self.player.decision_1_page <= 3:
            return self.round_number == 1

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
               'payoff': self.participant.payoff,
               }

    def before_next_page(self):

        if self.participant.vars['choice'] and not self.participant.vars['safe']:

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

            if self.player.decision_1_page == 1:
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

            if self.player.decision_1_page == 2:
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

            if self.player.decision_1_page == 3:
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

                self.participant.vars['payoff_a1'] = self.participant.vars['payoff_a1_1'] + self.participant.vars[
                    'payoff_a1_2'] + self.participant.vars['payoff_a1_3']
                self.participant.vars['urndraws1_a1'] = self.participant.vars['urndraws1_a1_1'] + '  ' + \
                                                        self.participant.vars['urndraws1_a1_2'] + '  ' + \
                                                        self.participant.vars['urndraws1_a1_3']
                self.participant.vars['urndraws2_a1'] = self.participant.vars['urndraws2_a1_1'] + '  ' + \
                                                        self.participant.vars['urndraws2_a1_2'] + '  ' + \
                                                        self.participant.vars['urndraws2_a1_3']
                self.participant.vars['urndraws3_a1'] = self.participant.vars['urndraws3_a1_1'] + '  ' + \
                                                        self.participant.vars['urndraws3_a1_2'] + '  ' + \
                                                        self.participant.vars['urndraws3_a1_3']
                self.participant.vars['option_1_a1'] = self.participant.vars['option_1_a1_1'] + self.participant.vars[
                    'option_1_a1_2'] + self.participant.vars['option_1_a1_3']
                self.participant.vars['option_2_a1'] = self.participant.vars['option_2_a1_1'] + self.participant.vars[
                    'option_2_a1_2'] + self.participant.vars['option_2_a1_3']
                self.participant.vars['option_3_a1'] = self.participant.vars['option_3_a1_1'] + self.participant.vars[
                    'option_3_a1_2'] + self.participant.vars['option_3_a1_3']

                self.participant.vars['payoff_1_a'] = self.participant.vars['payoff_1_a_1'] + self.participant.vars[
                    'payoff_1_a_2'] + self.participant.vars['payoff_1_a_3']
                self.participant.vars['payoff_2_a'] = self.participant.vars['payoff_2_a_1'] + self.participant.vars[
                    'payoff_2_a_2'] + self.participant.vars['payoff_2_a_3']
                self.participant.vars['payoff_3_a'] = self.participant.vars['payoff_3_a_1'] + self.participant.vars[
                    'payoff_3_a_2'] + self.participant.vars['payoff_3_a_3']

        elif not self.participant.vars['choice'] and not self.participant.vars['safe']:

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

        self.player.decision_1_page += 1

########################################################################################################################
# SAMPLING #############################################################################################################
########################################################################################################################

class SamplingTransition(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'incentive': self.participant.vars['incentive'],
               }

    def before_next_page(self):
        self.participant.payoff = 0


class Sampling(Page):
    form_model = 'player'
    def is_displayed(self):
        return self.round_number <= 10

    def get_form_fields(self):
        return ['option_1_samp', 'option_2_samp', 'option_3_samp']

    # def error_message(self, values):
    #     if self.participant.vars['choice'] or not self.participant.vars['choice']:
    #         if values['option_1_samp'] + values['option_2_samp'] + values['option_3_samp'] < 1:
    #             return 'You have to use your point to choose an urn.'
    #         elif values['option_1_samp'] + values['option_2_samp'] + values['option_3_samp'] > 1:
    #             return 'You can only choose one option per round.'

    def vars_for_template(self):
        return {'choice': self.participant.vars['choice'],
                'safe_option': Constants.safe_option,
                'endowment_choice': Constants.endowment_choice,
                'endowment_points': Constants.endowment_points,
                'draw': self.participant.vars['draw'],
                'feedback_3': self.participant.vars['feedback_3'],
                'incentive': self.participant.vars['incentive'],
                'sampling_round': self.player.sampling_round,

                }

    def before_next_page(self):

        Urn_1 = ['3', '4', '5', '6', '7', '8', '9', '10']
        Urn_2 = ['0', '1', '2', '3', '20', '25', '35', '40']
        Urn_3 = ['6']

        weights_1 = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
        weights_2 = [0.25, 0.25, 0.15, 0.15, 0.05, 0.05, 0.05, 0.05]
        weights_3 = [1]

        draws_1 = random.choices(Urn_1, weights=weights_1, k=self.player.option_1_samp)
        draws_2 = random.choices(Urn_2, weights=weights_2, k=self.player.option_2_samp)
        draws_3 = random.choices(Urn_3, weights=weights_3, k=self.player.option_3_samp)

        draws_1_str = str(draws_1)[1:-1]
        draws_2_str = str(draws_2)[1:-1]
        draws_3_str = str(draws_3)[1:-1]

        draws_1_str = draws_1_str.replace("'", "")
        draws_2_str = draws_2_str.replace("'", "")
        draws_3_str = draws_3_str.replace("'", "")

        self.player.urn_draws_1_samp = draws_1_str
        self.player.urn_draws_2_samp = draws_2_str
        self.player.urn_draws_3_samp = draws_3_str

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

        self.player.payoff_1_samp = 0
        self.player.payoff_2_samp = 0
        self.player.payoff_3_samp = 0

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

        self.player.payoff_1_samp = payoffs_1
        self.player.payoff_2_samp = payoffs_2
        self.player.payoff_3_samp = payoffs_3



class Feedback_Sampling(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number <= 10

    def vars_for_template(self):
        return {'choice': self.participant.vars['choice'],
                'draw': self.participant.vars['draw'],
                #'option_1_samp': self.player.option_1_samp,
                #'option_2_samp': self.player.option_2_samp,
                #'option_3_samp': self.player.option_3_samp,
                'urn_draws_1_samp': self.player.urn_draws_1_samp,
                'urn_draws_2_samp': self.player.urn_draws_2_samp,
                'urn_draws_3_samp': self.player.urn_draws_3_samp,
                'payoff_1_samp': self.player.payoff_1_samp,
                'payoff_2_samp': self.player.payoff_2_samp,
                'payoff_3_samp': self.player.payoff_3_samp,
                'payoff': self.player.payoff,

                }

    def before_next_page(self):
        if self.player.round_number == 10:
            payoff = int(self.participant.payoff)
            endowment = (payoff/10)
            print(endowment)
            endowment = Decimal(endowment).to_integral_value(rounding=ROUND_HALF_UP)
            print(endowment)
            self.player.endowment_after_sampling = int(endowment)
            print(self.player.endowment_after_sampling)


class Decision2Transition(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 10

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'payoff': self.participant.payoff,
               'endowment_samp': self.player.endowment_after_sampling,
               'incentive': self.participant.vars['incentive'],
               }

    def before_next_page(self):
        self.participant.payoff = 0

########################################################################################################################
# DECISION 2 ###########################################################################################################
########################################################################################################################

class Decision2(Page):
    form_model = 'player'

    def is_displayed(self):
        if not self.participant.vars['choice'] and self.player.decision_2_page == 1:
            return self.round_number == 10
        elif self.participant.vars['choice'] and self.player.decision_2_page <= 3:
            return self.round_number == 10

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
        if self.participant.vars['choice']:
            if values['option_1'] + values['option_2'] + values['option_3'] < 1:
                return 'You have to use your point to choose an urn.'
            elif values['option_1'] + values['option_2'] + values['option_3'] > 1:
                return 'You can only choose one option per round.'

        elif not self.participant.vars['choice']:
            if values['option_1'] + values['option_2'] + values['option_3'] < 3:
                return 'You have to use all three points'
            elif values['option_1'] + values['option_2'] + values['option_3'] > 3:
                return 'You can only use three points per round'

    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'safe_option': Constants.safe_option,
               'endowment_choice': Constants.endowment_choice,
               'endowment_points': Constants.endowment_points,
               'safe': self.participant.vars['safe'],
               'draw': self.participant.vars['draw'],
               'payoff': self.participant.payoff,
               }

    def before_next_page(self):

        if self.participant.vars['choice'] and not self.participant.vars['safe']:

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

            if self.player.decision_2_page == 1:
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

            if self.player.decision_2_page == 2:
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

            if self.player.decision_2_page == 3:
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
                self.participant.vars['urndraws1_b1'] = self.participant.vars['urndraws1_b1_1'] + '  ' + \
                                                        self.participant.vars['urndraws1_b1_2'] + '  ' + \
                                                        self.participant.vars['urndraws1_b1_3']
                self.participant.vars['urndraws2_b1'] = self.participant.vars['urndraws2_b1_1'] + '  ' + \
                                                        self.participant.vars['urndraws2_b1_2'] + '  ' + \
                                                        self.participant.vars['urndraws2_b1_3']
                self.participant.vars['urndraws3_b1'] = self.participant.vars['urndraws3_b1_1'] + '  ' + \
                                                        self.participant.vars['urndraws3_b1_2'] + '  ' + \
                                                        self.participant.vars['urndraws3_b1_3']
                self.participant.vars['option_1_b1'] = self.participant.vars['option_1_b1_1'] + self.participant.vars[
                    'option_1_b1_2'] + self.participant.vars['option_1_b1_3']
                self.participant.vars['option_2_b1'] = self.participant.vars['option_2_b1_1'] + self.participant.vars[
                    'option_2_b1_2'] + self.participant.vars['option_2_b1_3']
                self.participant.vars['option_3_b1'] = self.participant.vars['option_3_b1_1'] + self.participant.vars[
                    'option_3_b1_2'] + self.participant.vars['option_3_b1_3']

                self.participant.vars['payoff_1_b'] = self.participant.vars['payoff_1_b_1'] + self.participant.vars[
                    'payoff_1_b_2'] + self.participant.vars['payoff_1_b_3']
                self.participant.vars['payoff_2_b'] = self.participant.vars['payoff_2_b_1'] + self.participant.vars[
                    'payoff_2_b_2'] + self.participant.vars['payoff_2_b_3']
                self.participant.vars['payoff_3_b'] = self.participant.vars['payoff_3_b_1'] + self.participant.vars[
                    'payoff_3_b_2'] + self.participant.vars['payoff_3_b_3']

        elif not self.participant.vars['choice'] and not self.participant.vars['safe']:

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

        self.player.decision_2_page += 1


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
        return self.round_number == 10


    def vars_for_template(self):
        return{'questionnaire_page': self.player.questionnaire_page,
               'choice':self.participant.vars['choice'],
               'safe': self.participant.vars['safe'],
               'round': self.player.round_number,

               }

    def before_next_page(self):
        self.player.questionnaire_page += 1

        if self.player.questionnaire_page == 5:
            self.player.payoff_a = self.participant.vars['payoff_a1']
            self.player.payoff_b = self.participant.vars['payoff_b1']
            self.player.urn_draws_1_a = self.participant.vars['urndraws1_a1']
            self.player.urn_draws_1_b = self.participant.vars['urndraws1_b1']
            self.player.urn_draws_2_a = self.participant.vars['urndraws2_a1']
            self.player.urn_draws_2_b = self.participant.vars['urndraws2_b1']
            self.player.urn_draws_3_a = self.participant.vars['urndraws3_a1']
            self.player.urn_draws_3_b = self.participant.vars['urndraws3_b1']
            self.player.option_1_a = self.participant.vars['option_1_a1']
            self.player.option_1_b = self.participant.vars['option_1_b1']
            self.player.option_2_a = self.participant.vars['option_2_a1']
            self.player.option_2_b = self.participant.vars['option_2_b1']
            self.player.option_3_a = self.participant.vars['option_3_a1']
            self.player.option_3_b = self.participant.vars['option_3_b1']
            self.player.payoff_1_a = self.participant.vars['payoff_1_a']
            self.player.payoff_1_b = self.participant.vars['payoff_1_b']
            self.player.payoff_2_a = self.participant.vars['payoff_2_a']
            self.player.payoff_2_b = self.participant.vars['payoff_2_b']
            self.player.payoff_3_a = self.participant.vars['payoff_3_a']
            self.player.payoff_3_b = self.participant.vars['payoff_3_b']

            print(self.player.payoff_b)
            print(self.player.payoff_a)

        if self.player.questionnaire_page == 6:
            self.participant.payoff = self.player.payoff_b + self.player.payoff_a

            print(self.participant.payoff)
            print(self.player.payoff_b)
            print(self.player.payoff_a)


class Disclose_Payoff(Page):
    form_model ='player'

    def is_displayed(self):
        return self.round_number == 10


    def vars_for_template(self):
        return{'choice': self.participant.vars['choice'],
               'urn_draws_1_a': self.player.urn_draws_1_a,
               'urn_draws_2_a': self.player.urn_draws_2_a,
               'urn_draws_3_a': self.player.urn_draws_3_a,
               'urn_draws_1_b': self.player.urn_draws_1_b,
               'urn_draws_2_b': self.player.urn_draws_2_b,
               'urn_draws_3_b': self.player.urn_draws_3_b,
               'payoff_a': self.player.payoff_a,
               'payoff_b': self.player.payoff_b,
               'option_1_a': self.player.option_1_a,
               'option_1_b': self.player.option_1_b,
               'option_2_a': self.player.option_2_a,
               'option_2_b': self.player.option_2_b,
               'option_3_a': self.player.option_3_a,
               'option_3_b': self.player.option_3_b,
               'draw': self.participant.vars['draw'],
               'payoff_1_a': self.player.payoff_1_a,
               'payoff_1_b': self.player.payoff_1_b,
               'payoff_2_a': self.player.payoff_2_a,
               'payoff_2_b': self.player.payoff_2_b,
               'payoff_3_a': self.player.payoff_3_a,
               'payoff_3_b': self.player.payoff_3_b,
               }


class FinalInfo(Page):
    def is_displayed(self):
        return self.round_number == 10


    def vars_for_template(self):
        return {'participation_fee': self.session.config['participation_fee'],
                'total_payoff': self.participant.payoff_plus_participation_fee(),
                'bonus': self.participant.payoff.to_real_world_currency(self.session),
                'completion_code': self.participant.vars['completion_code'],
                }


page_sequence = [
    Device,
    AttentionCheck,
    DeadEnd,
    InstruStart,
    InstruStart,
    InstruStart,
    InstruStart,
    InstruStart,
    InstruStart,
    InstruStart,
    ComprehensionQuestions,
    ComprehensionQuestions,
    DeadEnd2,
    PriorsTransition,
    Priors,
    Decision,
    Decision,
    Decision,
    SamplingTransition,
    Sampling,
    Feedback_Sampling,
    Decision2Transition,
    Decision2,
    Decision2,
    Decision2,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    Disclose_Payoff,
    FinalInfo,
]
