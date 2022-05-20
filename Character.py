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

    def set_specific_stat(self, new_specific):
        self._chara_specific_type = new_specific

    def json_prepare(self):
        info_dict = {"kills": self._kills}
        info_dict["unconc"] = self._unconc
        info_dict["deaths"] = self._deaths
        info_dict["final_kills"] = self._final_kills
        info_dict["max_damage"] = self._max_damage_dealt
        info_dict["healing_dealt"] = self._healing_dealt
        info_dict["crit_success"] = self._crit_success
        info_dict["crit_fail"] = self._crit_fail
        info_dict["spec_count"] = self._chara_specific_count
        info_dict["spec_type"] = self._chara_specific_type
        info_dict["owner"] = self.owner_id


        char_dict = {self._name: info_dict}
        return char_dict


def json_rebuild(input_dict) -> Character:
    name = input_dict["name"]
    spec_type = input_dict["spec_type"]
    owner = input_dict["owner"]
    new_char = Character(name, spec_type, owner)

    new_char._kills = new_dict["kills"]
    new_char._unconc = new_dict["unconc"]
    new_char._deaths = new_dict["deaths"]
    new_char._final_kills = new_dict["final_kills"]
    new_char._max_damage_dealt = new_dict["max_damage"]
    new_char._healing_dealt = new_dict["healing_dealt"]
    new_char._crit_success = new_dict["crit_success"]
    new_char._crit_fail = new_dict["crit_fail"]
    new_char._chara_specific_count = new_dict["spec_count"]
