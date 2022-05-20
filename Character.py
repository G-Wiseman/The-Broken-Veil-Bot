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

    def set_specific_stat(self, new_specific):
        self._chara_specific_type = new_specific
