from card import CardTile

class Pilot
    def __init__(self):
        self.name = ""
        self.xp = 0 # for leveling up
        self.skill_level = 0 # enum for now
        self.aircraft_type = 0 # enum for now
        self.speed = 0 # can be slow or fast
        self.cannon_strike = 0 # combat in same hex
        self.stand_off = 0 # combat from distance
        self.cool = 0 # stress level
        self.okay = (0, 0) # self.okay[0] is always 0 and self.okay[1] is always > 0
        self.shaken = (0, 0) # from self.okay[1] + 1 to some value greater than that

class PilotCardTile(CardTile):
    def __init__(self, pilot=None):
        self.speed = 0
        self.strike = 0
        self.standoff = 0
        self.cool = 0
        self.stress = 0
        self.okay = (0, 0)
        self.shaken = (0, 0)

    def stats_text():
        stats = [f"Aim: {self.aim}", f"Speed: {self.speed}", f"Cool: {self.cool}"]

        for stat in stats:
            text = font.render(stat, True, (0, 0, 0))

def render(screen, cards, selected_cards)
    pass
