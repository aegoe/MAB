from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from django import forms

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'Pilot'
    num_rounds = 6
    num_rounds_choice = 6
    num_rounds_points = 2
    players_per_group = None
    endowment_choice = 1
    endowment_points = 3
    black = -1
    yellow = 0
    blue = 1
    green = 2
    white = -2
    # Urn_1 = [('Black', 1), ('Yellow', 5), ('Blue', 3), ('Green', 1)]
    # Urn_2 = [('Black', 1), ('Yellow', 3), ('Blue', 5), ('Green', 1)]
    # Urn_3 = [('White', 1), ('Yellow', 5), ('Black', 3), ('Green', 1)]
    safe_option = 3

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    choice = models.BooleanField()
    safe = models.BooleanField()
    endowment = models.IntegerField()
    option_1 = models.IntegerField(initial=None, label="Option X")
    option_2 = models.IntegerField(initial=None, label="Option Y")
    option_3 = models.IntegerField(initial=None, label="Option Z")
    option_safe = models.IntegerField(initial=None)
    #draws_1 = models.IntegerField()
    #draws_2 = models.IntegerField()
    #draws_3 = models.IntegerField()
    #count_1 = {}
    #count_2 = {}
    #count_3 = {}
    #data_counts = {}
    urn_draws_1 = models.StringField()
    urn_draws_2 = models.StringField()
    urn_draws_3 = models.StringField()
    urn_draws_4 = models.StringField()
    payoff = models.CurrencyField(initial=None)
    payoff_1 = models.CurrencyField()
    payoff_2 = models.CurrencyField()
    payoff_3 = models.CurrencyField()
    payoff_4 = models.CurrencyField()
    instru_page = models.IntegerField(initial=1)


    access_device = models.IntegerField(
        choices=[
            [0, 'Smartphone'],
            [1, 'Laptop'],
            [0, 'Tablet computer'],
            [1, 'Desktop PC'],
        ],
        widget=widgets.RadioSelect,
        blank=False,
        label="",
    )

    attention_check_1 = models.IntegerField(
        choices=[
            [0, 'Never'],
            [0, 'Less than once a month'],
            [0, '1-3 times a month'],
            [0, 'Once a week'],
            [0, '2-3 times a week'],
            [0, '4-5 times a week'],
            [0, 'More than 5 times a week'],
            [1, 'Other'],
        ],
        widget=widgets.RadioSelect,
        blank=False,
        label="",
    )

    attention_check_2 = models.StringField(blank=True)

    def option_1_max(self):
        if self.session.config['choice']:
            return Constants.endowment_choice
        else:
            return Constants.endowment_points

    def option_2_max(self):
        if self.session.config['choice']:
            return Constants.endowment_choice
        else:
            return Constants.endowment_points

    def option_3_max(self):
        if self.session.config['choice']:
            return Constants.endowment_choice
        else:
            return Constants.endowment_points

    def option_safe_max(self):
        if self.session.config['choice']:
            return Constants.endowment_choice
        else:
            return Constants.endowment_points
