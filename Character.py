class Character:
    def __init__(self, name, specific_stat : str ="None", owner:int = 0):
        self.owner_id = owner #The discord id of whoever claimed this character

        self._name = name
        self._kills = 0
        self._unconc = 0
        self._deaths = 0
        self._final_kills = 0
        self._max_damage_dealt = 0
        self._healing_dealt = 0
        self._crit_success = 0
        self._crit_fail = 0

        # This leaves room for one personalized stat to take,
        # will be decided upon creation of character, or could be changed
        self._chara_specific_count = 0
        self._chara_specific_type = specific_stat

    def __repr__(self):
        return f"Character named {self._name}"

    def show_current_stats(self):
        dashline = '--'*len(self._name)
        stats_display = f"{self._name}\n{dashline}\n"
        stats_display += f"Kills: {self._kills}\n"
        stats_display += f"Times unconscious: {self._unconc}\n"
        stats_display += f"Deaths: {self._deaths}\n"
        stats_display += f"Max Damage done in a turn: {self._max_damage_dealt}\n"
        stats_display += f"Healing Dealt: {self._healing_dealt}\n"
        stats_display += f"Natural Twenties: {self._crit_success}\n"
        stats_display += f"Natural Ones: {self._crit_fail}\n"
        stats_display += f"{self._chara_specific_type} : {self._chara_specific_count}\n"
        return stats_display
