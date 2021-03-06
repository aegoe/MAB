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
# Device ###############################################################################################################
########################################################################################################################

class Device(Page):
    def is_displayed(self):
        return self.round_number == 1

    form_model = 'player'
    form_fields = ['access_device']

    def before_next_page(self):
        if self.session.config['testing']:
            self.player.choice = self.participant.vars['choice'] = self.session.config['choice']
            self.player.safe = self.participant.vars['safe'] = self.session.config['safe']
            self.player.test_urns = self.participant.vars['test_urns'] = self.session.config['test_urns']
            letters_and_digits = string.ascii_letters + string.digits
            result_str = ''.join((random.choice(letters_and_digits) for i in range(7))) + str(random.randint(1, 8))
            self.player.completion_code = result_str
            self.participant.vars['completion_code'] = result_str

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

        elif self.session.config['name'] == 'MAB_Pilot_Study_Var_2_BRET':
            letters_and_digits = string.ascii_letters + string.digits
            result_str = ''.join((random.choice(letters_and_digits) for i in range(7))) + str(random.randint(1, 8))
            self.player.completion_code = result_str
            self.participant.vars['completion_code'] = result_str
            self.player.test_urns = self.participant.vars['test_urns'] = self.session.config['test_urns']
            self.player.variance = self.participant.vars['variance'] = self.session.config['variance']

            treatments = ['safe_choice', 'safe_no_choice', 'choice', 'no_choice']
            weights_2 = [0.5, 0.5, 0, 0]
            draw_2 = choice(treatments, 1, p=weights_2)
            self.participant.vars['draw_2'] = draw_2[0]
            if draw_2[0] == 'safe_choice':
                self.player.safe = self.participant.vars['safe'] = True
                self.player.choice = self.participant.vars['choice'] = True
            elif draw_2[0] == 'safe_no_choice':
                self.player.safe = self.participant.vars['safe'] = True
                self.player.choice = self.participant.vars['choice'] = False
            elif draw_2[0] == 'choice':
                self.player.safe = self.participant.vars['safe'] = False
                self.player.choice = self.participant.vars['choice'] = True
            else:
                self.player.safe = self.participant.vars['safe'] = False
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
                'conversion_factor': int(self.session.config['real_world_currency_per_point'] * 1000),
                'choice': self.participant.vars['choice'],
                'safe': self.participant.vars['safe'],
                'endowment_choice': Constants.endowment_choice,
                'endowment_points': Constants.endowment_points,
                'draw': self.participant.vars['draw'],
                'test_urns': self.participant.vars['test_urns'],
                'variance': self.participant.vars['variance'],

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
                'variance': self.participant.vars['variance'],
                }

    def get_form_fields(self):
        if self.participant.vars['choice'] and not self.participant.vars['variance']:
            return ['cq_Pilot_1', 'cq_Pilot_2', 'cq_Pilot_3']
        elif not self.participant.vars['choice'] and not self.participant.vars['variance']:
                return ['cq_Pilot_1', 'cq_Pilot_2', 'cq_Pilot_3', 'cq_Pilot_4']
        elif self.participant.vars['choice'] and  self.participant.vars['variance']:
            return ['cq_Pilot_1', 'cq_Pilot_2', 'cq_Pilot_5']
        elif not self.participant.vars['choice'] and  self.participant.vars['variance']:
            return ['cq_Pilot_1', 'cq_Pilot_2', 'cq_Pilot_4', 'cq_Pilot_5']

    def before_next_page(self):
        if self.participant.vars['choice']:
            if sum([self.player.cq_Pilot_1, self.player.cq_Pilot_2, self.player.cq_Pilot_3]) < 4:
                self.player.controls = 1
        else:
            if sum([self.player.cq_Pilot_1, self.player.cq_Pilot_2, self.player.cq_Pilot_3, self.player.cq_Pilot_4]) < 5:
                self.player.controls = 1

        self.player.comprehension_page += 1


class DeadEnd2(Page):
    def is_displayed(self) -> bool:
        return self.player.in_round(1).controls !=1 and self.round_number == 1






########################################################################################################################
# DECISION ## ##########################################################################################################
########################################################################################################################

class Decision(Page):
    form_model = 'player'

    def is_displayed(self):
        if self.participant.vars['choice']:
            return self.round_number <= Constants.num_rounds_choice
        else:
            return self.round_number <= Constants.num_rounds_points

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
               }

    def before_next_page(self):

        if self.participant.vars['choice'] and not self.participant.vars['safe'] and not self.participant.vars['test_urns'] and not self.participant.vars['variance']:

            Urn_1 = ['-4', '-3', '4', '12']
            Urn_2 = ['-4', '4', '11', '12']
            Urn_3 = ['-7', '-6', '1', '9']

            weights_1 = [0.125, 0.125, 0.39063, 0.35937]
            weights_2 = [0.35937, 0.39063, 0.125, 0.125]
            weights_3 = [0.125, 0.125, 0.39063, 0.35937]

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
                    if k == '-7':
                        data_counts[i][k] = v * Constants.a
                    elif k == '-6':
                        data_counts[i][k] = v * Constants.b
                    elif k == '-4':
                        data_counts[i][k] = v * Constants.c
                    elif k == '-3':
                        data_counts[i][k] = v * Constants.d
                    elif k == '1':
                        data_counts[i][k] = v * Constants.e
                    elif k == '4':
                        data_counts[i][k] = v * Constants.f
                    elif k == '9':
                        data_counts[i][k] = v * Constants.g
                    elif k == '11':
                        data_counts[i][k] = v * Constants.h
                    elif k == '12':
                        data_counts[i][k] = v * Constants.i

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

        elif self.participant.vars['choice'] and self.participant.vars['safe'] and not self.participant.vars['test_urns'] and not self.participant.vars['variance']:

            Urn_1 = ['-4', '-3', '4', '12']
            Urn_2 = ['-4', '4', '11', '12']
            Urn_3 = ['-7', '-6', '1', '9']
            Urn_safe = ['4']

            weights_1 = [0.125, 0.125, 0.39063, 0.35937]
            weights_2 = [0.35937, 0.39063, 0.125, 0.125]
            weights_3 = [0.125, 0.125, 0.39063, 0.35937]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)
            draws_4 = random.choices(Urn_safe, k = self.player.option_safe)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]
            draws_4_str = str(draws_4)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")
            draws_4_str = draws_4_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str
            self.player.urn_draws_4 = draws_4_str

            print(self.player.urn_draws_1)
            print(draws_1)
            print(draws_2)
            print(draws_3)

            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)
            count_4 = Counter(draws_4)

            print(count_1)
            print(count_2)
            print(count_3)



            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3
            data_counts['count_4'] = count_4

            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '-7':
                        data_counts[i][k] = v * Constants.a
                    elif k == '-6':
                        data_counts[i][k] = v * Constants.b
                    elif k == '-4':
                        data_counts[i][k] = v * Constants.c
                    elif k == '-3':
                        data_counts[i][k] = v * Constants.d
                    elif k == '1':
                        data_counts[i][k] = v * Constants.e
                    elif k == '4':
                        data_counts[i][k] = v * Constants.f
                    elif k == '9':
                        data_counts[i][k] = v * Constants.g
                    elif k == '11':
                        data_counts[i][k] = v * Constants.h
                    elif k == '12':
                        data_counts[i][k] = v * Constants.i
                    elif k == '4':
                        data_counts[i][k] = v * Constants.safe_option

            self.player.payoff = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    self.player.payoff += values

            print(data_counts)

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0
            self.player.payoff_4 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        self.player.payoff_1 += v
                    if i == 'count_2':
                        self.player.payoff_2 += v
                    if i == 'count_3':
                        self.player.payoff_3 += v
                    if i == 'count_4':
                        self.player.payoff_4 += v

            print(self.player.payoff)
            print(self.participant.payoff)

        elif not self.participant.vars['choice'] and not self.participant.vars['safe'] and not self.participant.vars['test_urns'] and not self.participant.vars['variance']:

            Urn_1 = ['-4', '-3', '4', '12']
            Urn_2 = ['-4', '4', '11', '12']
            Urn_3 = ['-7', '-6', '1', '9']

            weights_1 = [0.125, 0.125, 0.39063, 0.35937]
            weights_2 = [0.35937, 0.39063, 0.125, 0.125]
            weights_3 = [0.125, 0.125, 0.39063, 0.35937]

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
                    if k == '-7':
                        data_counts[i][k] = v * Constants.a
                    elif k == '-6':
                        data_counts[i][k] = v * Constants.b
                    elif k == '-4':
                        data_counts[i][k] = v * Constants.c
                    elif k == '-3':
                        data_counts[i][k] = v * Constants.d
                    elif k == '1':
                        data_counts[i][k] = v * Constants.e
                    elif k == '4':
                        data_counts[i][k] = v * Constants.f
                    elif k == '9':
                        data_counts[i][k] = v * Constants.g
                    elif k == '11':
                        data_counts[i][k] = v * Constants.h
                    elif k == '12':
                        data_counts[i][k] = v * Constants.i

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

        elif not self.participant.vars['choice'] and self.participant.vars['safe'] and not self.participant.vars['test_urns'] and not self.participant.vars['variance']:

            Urn_1 = ['-4', '-3', '4', '12']
            Urn_2 = ['-4', '4', '11', '12']
            Urn_3 = ['-7', '-6', '1', '9']
            Urn_safe = ['4']

            weights_1 = [0.125, 0.125, 0.39063, 0.35937]
            weights_2 = [0.35937, 0.39063, 0.125, 0.125]
            weights_3 = [0.125, 0.125, 0.39063, 0.35937]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)
            draws_4 = random.choices(Urn_safe, k = self.player.option_safe)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]
            draws_4_str = str(draws_4)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")
            draws_4_str = draws_4_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str
            self.player.urn_draws_4 = draws_4_str

            print(self.player.urn_draws_1)
            print(draws_1)
            print(draws_2)
            print(draws_3)

            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)
            count_4 = Counter(draws_4)

            print(count_1)
            print(count_2)
            print(count_3)



            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3
            data_counts['count_4'] = count_4

            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '-7':
                        data_counts[i][k] = v * Constants.a
                    elif k == '-6':
                        data_counts[i][k] = v * Constants.b
                    elif k == '-4':
                        data_counts[i][k] = v * Constants.c
                    elif k == '-3':
                        data_counts[i][k] = v * Constants.d
                    elif k == '1':
                        data_counts[i][k] = v * Constants.e
                    elif k == '4':
                        data_counts[i][k] = v * Constants.f
                    elif k == '9':
                        data_counts[i][k] = v * Constants.g
                    elif k == '11':
                        data_counts[i][k] = v * Constants.h
                    elif k == '12':
                        data_counts[i][k] = v * Constants.i
                    elif k == '4':
                        data_counts[i][k] = v * Constants.safe_option

            self.player.payoff = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    self.player.payoff += values

            print(data_counts)

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0
            self.player.payoff_4 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        self.player.payoff_1 += v
                    if i == 'count_2':
                        self.player.payoff_2 += v
                    if i == 'count_3':
                        self.player.payoff_3 += v
                    if i == 'count_4':
                        self.player.payoff_4 += v

            print(self.player.payoff)
            print(self.participant.payoff)

        elif not self.participant.vars['choice'] and self.participant.vars['safe'] and self.participant.vars['test_urns'] and not self.participant.vars['variance']:

            Urn_1 = ['-2', '-1', '7', '8']
            Urn_2 = ['-3', '-2', '6', '7']
            Urn_3 = ['-5', '-4', '4', '5']
            Urn_safe = ['3']

            weights_1 = [0.25, 0.25, 0.25, 0.25]
            weights_2 = [0.25, 0.25, 0.25, 0.25]
            weights_3 = [0.25, 0.25, 0.25, 0.25]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)
            draws_4 = random.choices(Urn_safe, k = self.player.option_safe)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]
            draws_4_str = str(draws_4)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")
            draws_4_str = draws_4_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str
            self.player.urn_draws_4 = draws_4_str

            print(self.player.urn_draws_1)
            print(draws_1)
            print(draws_2)
            print(draws_3)

            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)
            count_4 = Counter(draws_4)

            print(count_1)
            print(count_2)
            print(count_3)



            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3
            data_counts['count_4'] = count_4

            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '-5':
                        data_counts[i][k] = v * -5
                    elif k == '-4':
                        data_counts[i][k] = v * -4
                    elif k == '-3':
                        data_counts[i][k] = v * -3
                    elif k == '-2':
                        data_counts[i][k] = v * -2
                    elif k == '-1':
                        data_counts[i][k] = v * -1
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
                    elif k == '3':
                        data_counts[i][k] = v * 3

            self.player.payoff = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    self.player.payoff += values

            print(data_counts)

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0
            self.player.payoff_4 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        self.player.payoff_1 += v
                    if i == 'count_2':
                        self.player.payoff_2 += v
                    if i == 'count_3':
                        self.player.payoff_3 += v
                    if i == 'count_4':
                        self.player.payoff_4 += v

            print(self.player.payoff)
            print(self.participant.payoff)

        elif self.participant.vars['choice'] and self.participant.vars['safe'] and self.participant.vars['test_urns'] and not self.participant.vars['variance']:

            Urn_1 = ['-2', '-1', '7', '8']
            Urn_2 = ['-3', '-2', '6', '7']
            Urn_3 = ['-5', '-4', '4', '5']
            Urn_safe = ['3']

            weights_1 = [0.25, 0.25, 0.25, 0.25]
            weights_2 = [0.25, 0.25, 0.25, 0.25]
            weights_3 = [0.25, 0.25, 0.25, 0.25]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)
            draws_4 = random.choices(Urn_safe, k = self.player.option_safe)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]
            draws_4_str = str(draws_4)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")
            draws_4_str = draws_4_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str
            self.player.urn_draws_4 = draws_4_str

            print(self.player.urn_draws_1)
            print(draws_1)
            print(draws_2)
            print(draws_3)

            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)
            count_4 = Counter(draws_4)

            print(count_1)
            print(count_2)
            print(count_3)



            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3
            data_counts['count_4'] = count_4

            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '-5':
                        data_counts[i][k] = v * -5
                    elif k == '-4':
                        data_counts[i][k] = v * -4
                    elif k == '-3':
                        data_counts[i][k] = v * -3
                    elif k == '-2':
                        data_counts[i][k] = v * -2
                    elif k == '-1':
                        data_counts[i][k] = v * -1
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
                    elif k == '3':
                        data_counts[i][k] = v * 3

            self.player.payoff = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    self.player.payoff += values

            print(data_counts)

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0
            self.player.payoff_4 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        self.player.payoff_1 += v
                    if i == 'count_2':
                        self.player.payoff_2 += v
                    if i == 'count_3':
                        self.player.payoff_3 += v
                    if i == 'count_4':
                        self.player.payoff_4 += v

            print(self.player.payoff)
            print(self.participant.payoff)

        elif self.participant.vars['choice'] and self.participant.vars['safe'] and not self.participant.vars['test_urns'] and self.participant.vars['variance']:

            Urn_1 = ['5', '2', '-1', '-2']
            Urn_2 = ['6', '3', '-2', '-3']
            Urn_3 = ['7', '4', '-3', '-4']
            Urn_safe = ['1']

            weights_1 = [0.25, 0.25, 0.25, 0.25]
            weights_2 = [0.25, 0.25, 0.25, 0.25]
            weights_3 = [0.25, 0.25, 0.25, 0.25]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)
            draws_4 = random.choices(Urn_safe, k = self.player.option_safe)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]
            draws_4_str = str(draws_4)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")
            draws_4_str = draws_4_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str
            self.player.urn_draws_4 = draws_4_str

            print(self.player.urn_draws_1)
            print(draws_1)
            print(draws_2)
            print(draws_3)

            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)
            count_4 = Counter(draws_4)

            print(count_1)
            print(count_2)
            print(count_3)



            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3
            data_counts['count_4'] = count_4

            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '7':
                        data_counts[i][k] = v * 7
                    elif k == '6':
                        data_counts[i][k] = v * 6
                    elif k == '5':
                        data_counts[i][k] = v * 5
                    elif k == '4':
                        data_counts[i][k] = v * 4
                    elif k == '3':
                        data_counts[i][k] = v * 3
                    elif k == '2':
                        data_counts[i][k] = v * 2
                    elif k == '-1':
                        data_counts[i][k] = v * -1
                    elif k == '-2':
                        data_counts[i][k] = v * -2
                    elif k == '-3':
                        data_counts[i][k] = v * -3
                    elif k == '-4':
                        data_counts[i][k] = v * -4
                    elif k == '1':
                        data_counts[i][k] = v * 1

            self.player.payoff = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    self.player.payoff += values

            print(data_counts)

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0
            self.player.payoff_4 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        self.player.payoff_1 += v
                    if i == 'count_2':
                        self.player.payoff_2 += v
                    if i == 'count_3':
                        self.player.payoff_3 += v
                    if i == 'count_4':
                        self.player.payoff_4 += v

            print(self.player.payoff)
            print(self.participant.payoff)

        elif not self.participant.vars['choice'] and self.participant.vars['safe'] and not self.participant.vars['test_urns'] and self.participant.vars['variance']:

            Urn_1 = ['5', '2', '-1', '-2']
            Urn_2 = ['6', '3', '-2', '-3']
            Urn_3 = ['7', '4', '-3', '-4']
            Urn_safe = ['1']

            weights_1 = [0.25, 0.25, 0.25, 0.25]
            weights_2 = [0.25, 0.25, 0.25, 0.25]
            weights_3 = [0.25, 0.25, 0.25, 0.25]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)
            draws_4 = random.choices(Urn_safe, k = self.player.option_safe)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]
            draws_4_str = str(draws_4)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")
            draws_4_str = draws_4_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str
            self.player.urn_draws_4 = draws_4_str

            print(self.player.urn_draws_1)
            print(draws_1)
            print(draws_2)
            print(draws_3)

            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)
            count_4 = Counter(draws_4)

            print(count_1)
            print(count_2)
            print(count_3)



            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3
            data_counts['count_4'] = count_4

            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '7':
                        data_counts[i][k] = v * 7
                    elif k == '6':
                        data_counts[i][k] = v * 6
                    elif k == '5':
                        data_counts[i][k] = v * 5
                    elif k == '4':
                        data_counts[i][k] = v * 4
                    elif k == '3':
                        data_counts[i][k] = v * 3
                    elif k == '2':
                        data_counts[i][k] = v * 2
                    elif k == '-1':
                        data_counts[i][k] = v * -1
                    elif k == '-2':
                        data_counts[i][k] = v * -2
                    elif k == '-3':
                        data_counts[i][k] = v * -3
                    elif k == '-4':
                        data_counts[i][k] = v * -4
                    elif k == '1':
                        data_counts[i][k] = v * 1

            self.player.payoff = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    self.player.payoff += values

            print(data_counts)

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0
            self.player.payoff_4 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        self.player.payoff_1 += v
                    if i == 'count_2':
                        self.player.payoff_2 += v
                    if i == 'count_3':
                        self.player.payoff_3 += v
                    if i == 'count_4':
                        self.player.payoff_4 += v

            print(self.player.payoff)
            print(self.participant.payoff)

        elif self.participant.vars['choice'] and self.participant.vars['safe'] and self.participant.vars['test_urns'] and self.participant.vars['variance']:

            Urn_1 = ['5', '3', '2', '-2']
            Urn_2 = ['7', '3', '2', '-4']
            Urn_3 = ['9', '3', '2', '-6']
            Urn_safe = ['2']

            weights_1 = [0.25, 0.25, 0.25, 0.25]
            weights_2 = [0.25, 0.25, 0.25, 0.25]
            weights_3 = [0.25, 0.25, 0.25, 0.25]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)
            draws_4 = random.choices(Urn_safe, k = self.player.option_safe)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]
            draws_4_str = str(draws_4)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")
            draws_4_str = draws_4_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str
            self.player.urn_draws_4 = draws_4_str

            print(self.player.urn_draws_1)
            print(draws_1)
            print(draws_2)
            print(draws_3)

            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)
            count_4 = Counter(draws_4)

            print(count_1)
            print(count_2)
            print(count_3)



            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3
            data_counts['count_4'] = count_4

            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '9':
                        data_counts[i][k] = v * 9
                    elif k == '7':
                        data_counts[i][k] = v * 7
                    elif k == '5':
                        data_counts[i][k] = v * 5
                    elif k == '3':
                        data_counts[i][k] = v * 3
                    elif k == '2':
                        data_counts[i][k] = v * 2
                    elif k == '-2':
                        data_counts[i][k] = v * -2
                    elif k == '-4':
                        data_counts[i][k] = v * -4
                    elif k == '-6':
                        data_counts[i][k] = v * -6

            self.player.payoff = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    self.player.payoff += values

            print(data_counts)

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0
            self.player.payoff_4 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        self.player.payoff_1 += v
                    if i == 'count_2':
                        self.player.payoff_2 += v
                    if i == 'count_3':
                        self.player.payoff_3 += v
                    if i == 'count_4':
                        self.player.payoff_4 += v

            print(self.player.payoff)
            print(self.participant.payoff)

        elif not self.participant.vars['choice'] and self.participant.vars['safe'] and self.participant.vars['test_urns'] and self.participant.vars['variance']:

            Urn_1 = ['5', '3', '2', '-2']
            Urn_2 = ['7', '3', '2', '-4']
            Urn_3 = ['9', '3', '2', '-6']
            Urn_safe = ['2']

            weights_1 = [0.25, 0.25, 0.25, 0.25]
            weights_2 = [0.25, 0.25, 0.25, 0.25]
            weights_3 = [0.25, 0.25, 0.25, 0.25]

            draws_1 = random.choices(Urn_1, weights=weights_1, k = self.player.option_1)
            draws_2 = random.choices(Urn_2, weights=weights_2, k = self.player.option_2)
            draws_3 = random.choices(Urn_3, weights=weights_3, k = self.player.option_3)
            draws_4 = random.choices(Urn_safe, k = self.player.option_safe)

            draws_1_str = str(draws_1)[1:-1]
            draws_2_str = str(draws_2)[1:-1]
            draws_3_str = str(draws_3)[1:-1]
            draws_4_str = str(draws_4)[1:-1]

            draws_1_str = draws_1_str.replace("'","")
            draws_2_str = draws_2_str.replace("'","")
            draws_3_str = draws_3_str.replace("'","")
            draws_4_str = draws_4_str.replace("'","")

            self.player.urn_draws_1 = draws_1_str
            self.player.urn_draws_2 = draws_2_str
            self.player.urn_draws_3 = draws_3_str
            self.player.urn_draws_4 = draws_4_str

            print(self.player.urn_draws_1)
            print(draws_1)
            print(draws_2)
            print(draws_3)

            count_1 = Counter(draws_1)
            count_2 = Counter(draws_2)
            count_3 = Counter(draws_3)
            count_4 = Counter(draws_4)

            print(count_1)
            print(count_2)
            print(count_3)



            data_counts = {}
            data_counts['count_1'] = count_1
            data_counts['count_2'] = count_2
            data_counts['count_3'] = count_3
            data_counts['count_4'] = count_4

            for i in data_counts.keys():
                for k, v in data_counts[i].items():
                    if k == '9':
                        data_counts[i][k] = v * 9
                    elif k == '7':
                        data_counts[i][k] = v * 7
                    elif k == '5':
                        data_counts[i][k] = v * 5
                    elif k == '3':
                        data_counts[i][k] = v * 3
                    elif k == '2':
                        data_counts[i][k] = v * 2
                    elif k == '-2':
                        data_counts[i][k] = v * -2
                    elif k == '-4':
                        data_counts[i][k] = v * -4
                    elif k == '-6':
                        data_counts[i][k] = v * -6

            self.player.payoff = 0
            for i in data_counts.keys():
                for values in data_counts[i].values():
                    self.player.payoff += values

            print(data_counts)

            self.player.payoff_1 = 0
            self.player.payoff_2 = 0
            self.player.payoff_3 = 0
            self.player.payoff_4 = 0

            for i in data_counts.keys():
                for v in data_counts[i].values():
                    if i == 'count_1':
                        self.player.payoff_1 += v
                    if i == 'count_2':
                        self.player.payoff_2 += v
                    if i == 'count_3':
                        self.player.payoff_3 += v
                    if i == 'count_4':
                        self.player.payoff_4 += v

            print(self.player.payoff)
            print(self.participant.payoff)


class Feedback(Page):
    form_model = 'player'
    #form_fields = ['option_1', 'option_2', 'option_3']

    def is_displayed(self):
        if self.participant.vars['choice']:
            return self.round_number <= Constants.num_rounds_choice
        else:
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

                }


########################################################################################################################
# Questionnaire and Final Page #########################################################################################
########################################################################################################################


class Questionnaire(Page):
    form_model ='player'

    def get_form_fields(self):
        if self.participant.vars['choice'] and self.participant.vars['safe'] and not self.participant.vars['variance']:
            if self.player.questionnaire_page == 1:
                return[]
            elif self.player.questionnaire_page == 2:
                return ['q_risk']
            elif self.player.questionnaire_page == 3:
                imi = [f'q_imi_{i}' for i in range(1, 8)]
                return imi
            elif self.player.questionnaire_page == 4:
                return ['q_exploration_strategy', 'q_maxoption', 'q_firm']
            elif self.player.questionnaire_page == 5:
                return ['q_fadein', 'q_fadeout']
            elif self.player.questionnaire_page == 6:
                return ['q_saving', 'q_wealth']
            elif self.player.questionnaire_page == 7:
                return ['q_year', 'q_sex', 'q_employment', 'q_education',
                        'q_ethnicity']

        elif self.participant.vars['choice'] and not self.participant.vars['safe'] and not self.participant.vars['variance']:
            if self.player.questionnaire_page == 1:
                return[]
            elif self.player.questionnaire_page == 2:
                return ['q_risk']
            elif self.player.questionnaire_page == 3:
                imi = [f'q_imi_{i}' for i in range(1, 8)]
                return imi
            elif self.player.questionnaire_page == 4:
                return ['q_exploration_strategy', 'q_maxoption_2', 'q_firm']
            elif self.player.questionnaire_page == 5:
                return ['q_fadein', 'q_fadeout']
            elif self.player.questionnaire_page == 6:
                return ['q_saving', 'q_wealth']
            elif self.player.questionnaire_page == 7:
                return ['q_year', 'q_sex', 'q_employment', 'q_education',
                        'q_ethnicity']

        elif not self.participant.vars['choice'] and self.participant.vars['safe'] and not self.participant.vars['variance']:
            if self.player.questionnaire_page == 1:
                return[]
            elif self.player.questionnaire_page == 2:
                return ['q_risk']
            elif self.player.questionnaire_page == 3:
                imi = [f'q_imi_{i}' for i in range(1, 8)]
                return imi
            elif self.player.questionnaire_page == 4:
                return ['q_exploration_strategy', 'q_maxoption', 'q_firm']
            elif self.player.questionnaire_page == 5:
                return ['q_fadein', 'q_fadeout']
            elif self.player.questionnaire_page == 6:
                return ['q_saving', 'q_wealth']
            elif self.player.questionnaire_page == 7:
                return ['q_year', 'q_sex', 'q_employment', 'q_education',
                        'q_ethnicity']

        elif not self.participant.vars['choice'] and not self.participant.vars['safe'] and not self.participant.vars['variance']:
            if self.player.questionnaire_page == 1:
                return[]
            elif self.player.questionnaire_page == 2:
                return ['q_risk']
            elif self.player.questionnaire_page == 3:
                imi = [f'q_imi_{i}' for i in range(1, 8)]
                return imi
            elif self.player.questionnaire_page == 4:
                return ['q_exploration_strategy', 'q_maxoption_2', 'q_firm']
            elif self.player.questionnaire_page == 5:
                return ['q_fadein', 'q_fadeout']
            elif self.player.questionnaire_page == 6:
                return ['q_saving', 'q_wealth']
            elif self.player.questionnaire_page == 7:
                return ['q_year', 'q_sex', 'q_employment', 'q_education',
                        'q_ethnicity']

        elif not self.participant.vars['choice'] and self.participant.vars['safe'] and self.participant.vars['variance']:
            if self.player.questionnaire_page == 1:
                return[]
            elif self.player.questionnaire_page == 2:
                return ['q_risk']
            elif self.player.questionnaire_page == 3:
                imi = [f'q_imi_{i}' for i in range(1, 8)]
                return imi
            elif self.player.questionnaire_page == 4:
                return ['q_exploration_strategy', 'q_maxoption', 'q_firm']
            elif self.player.questionnaire_page == 5:
                return ['q_fadein', 'q_fadeout']
            elif self.player.questionnaire_page == 6:
                return ['q_saving', 'q_wealth']
            elif self.player.questionnaire_page == 7:
                return ['q_year', 'q_sex', 'q_employment', 'q_education',
                        'q_ethnicity']

        elif self.participant.vars['choice'] and self.participant.vars['safe'] and self.participant.vars['variance']:
            if self.player.questionnaire_page == 1:
                return[]
            elif self.player.questionnaire_page == 2:
                return ['q_risk']
            elif self.player.questionnaire_page == 3:
                imi = [f'q_imi_{i}' for i in range(1, 8)]
                return imi
            elif self.player.questionnaire_page == 4:
                return ['q_exploration_strategy', 'q_maxoption', 'q_firm']
            elif self.player.questionnaire_page == 5:
                return ['q_fadein', 'q_fadeout']
            elif self.player.questionnaire_page == 6:
                return ['q_saving', 'q_wealth']
            elif self.player.questionnaire_page == 7:
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
               'variance': self.participant.vars['variance'],

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
                'total_payoff': self.participant.payoff_plus_participation_fee(),
                'bonus': self.participant.payoff.to_real_world_currency(self.session),
                'completion_code': self.participant.vars['completion_code'],
                }


page_sequence = [
    Device,
    #AttentionCheck,
    #DeadEnd,
    InstruStart,
    InstruStart,
    InstruStart,
    InstruStart,
    ComprehensionQuestions,
    ComprehensionQuestions,
    DeadEnd2,
    Decision,
    Feedback,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    Questionnaire,
    #FinalInfo,
]
