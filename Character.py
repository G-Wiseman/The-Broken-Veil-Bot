class Character:
    def __init__(self, name, specific_stat : str ="None", owner:int = 0):
        self.owner_id = owner #The discord id of whoever claimed this character

        self._name = name # Sets the name of the character

        # Set all the new character's stats to
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

    def __repr__(self) -> str:
        return f"Character with name {self._name}"

    def show_current_stats(self) -> str:
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

    def get_name(self):
        return self.name

    def get_kills(self):
        return self._kills
    def set_kills(self, new_value:int):
        self._kills = new_value

    def get_unconc(self):
        return self._unconc
    def set_unconc(self, new_value:int):
        self._unconc = new_value

    def get_deaths(self):
        return self._deaths
    def set_deaths(self, new_value:int):
        self._deaths = new_value

    def get_finals(self):
        return self._final_kills
    def set_finals(self, new_value:int):
        self._final_kills = new_value

    def get_max_damage(self):
        return self._max_damage_dealt
    def set_max_damage(self, new_value:int):
        self._max_damage_dealt = new_value

    def get_healing(self):
        return self._healing_dealt
    def set_healing(self, new_value:int):
        self._healing_dealt = new_value

    def get_crit_success(self):
        return self._crit_success
    def set_crit_success(self, new_value:int):
        self._crit_success = new_value

    def get_crit_fail(self):
        return self._crit_fail
    def set_deaths(self, new_value:int):
        self._crit_fail = new_value

    def get_spec_type(self):
        return self._chara_specific_type
    def set_deaths(self, new_value:str):
        self._chara_specific_type = new_value

    def get_spec_count(self):
        return self._chara_specific_count
    def set_spec_count(self, new_value:int):
        self._chara_specific_count = new_value


def remake_char(old_char)->Character:
    """
    Remakes the character object, allowing for changes to be
    made to the Character class, without the pickled data being
    "left behind".
    Returns a new character object that matches the character object
    passed, but with any new changes to the Character Class reflected.
    """

    char_name = old_char._name
    spec_stat_type = old_char._chara_specific_type
    owner = old_char.owner_id
    new_char = Character(char_name, spec_stat_type, owner)

    new_char._kills                = old_char._kills
    new_char._unconc               = old_char._unconc
    new_char._deaths               = old_char._deaths
    new_char._final_kills          = old_char._final_kills
    new_char._max_damage_dealt     = old_char._max_damage_dealt
    new_char._healing_dealt        = old_char._healing_dealt
    new_char._crit_success         = old_char._crit_success
    new_char._crit_fail            = old_char._crit_fail
    new_char._chara_specific_count = old_char._chara_specific_count

    return new_char
