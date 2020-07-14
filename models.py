from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'MAB'
    num_rounds_choice = 210
    num_rounds_points = 70
    players_per_group = None
    endowment_choice = 1
    endowment_points = 3
    black = -1
    yellow = 0
    blue = 1
    green = 2
    white = -2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

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
