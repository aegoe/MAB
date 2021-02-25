# Don't change anything in this file.
from Pilot import models
import otree.api


class Page(otree.api.Page):
    subsession: models.Subsession
    group: models.Group
    player: models.Player


class WaitPage(otree.api.WaitPage):
    subsession: models.Subsession
    group: models.Group


class Bot(otree.api.Bot):
    subsession: models.Subsession
    group: models.Group
    player: models.Player
