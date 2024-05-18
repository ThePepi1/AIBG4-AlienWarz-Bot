import json


class Player:
    RAW_DIAMOND_WEIGHT = 5
    PROCESSED_DIAMOND_WEIGHT = 3
    RAW_MINERAL_WEIGHT = 2
    PROCESSED_MINERAL_WEIGHT = 1

    def __init__(self):
        self.name = "Player"
        self.energy = 1000
        self.xp = 0
        self.coins = 100
        self.position = [0, 0]
        self.increased_backpack_duration = 0
        self.daze_turns = 0
        self.frozen_turns = 0
        self.backpack_capacity = 0
        self.raw_minerals = 0
        self.processed_minerals = 0
        self.raw_diamonds = 0
        self.processed_diamonds = 0
        
    def update(self, parsed_data):
        self.name = parsed_data["name"]
        self.energy = parsed_data["energy"]
        self.xp = parsed_data["xp"]
        self.coins = parsed_data["coins"]
        self.position = tuple(parsed_data["position"])
        self.increased_backpack_duration = parsed_data["increased_backpack_duration"]
        self.daze_turns = parsed_data["daze_turns"]
        self.frozen_turns = parsed_data["frozen_turns"]
        self.backpack_capacity = parsed_data["backpack_capacity"]
        self.raw_minerals = parsed_data["raw_minerals"]
        self.processed_minerals = parsed_data["processed_minerals"]
        self.raw_diamonds = parsed_data["raw_diamonds"]
        self.processed_diamonds = parsed_data["processed_diamonds"]

    def isDazed(self):
        return self.daze_turns > 0

    def isFrozen(self):
        return self.frozen_turns > 0
    
    def backpackWeight(self):
        return self.raw_minerals * self.RAW_MINERAL_WEIGHT + self.processed_minerals * self.PROCESSED_MINERAL_WEIGHT + self.raw_diamonds * self.RAW_DIAMOND_WEIGHT + self.processed_diamonds * self.PROCESSED_DIAMOND_WEIGHT

    def __str__(self) -> str:
        return json.dumps({
            "name": self.name,
            "energy": self.energy,
            "xp": self.xp,
            "coins": self.coins,
            "position": self.position,
            "increased_backpack_duration": self.increased_backpack_duration,
            "daze_turns": self.daze_turns,
            "frozen_turns": self.frozen_turns,
            "backpack_capacity": self.backpack_capacity,
            "raw_minerals": self.raw_minerals,
            "processed_minerals": self.processed_minerals,
            "raw_diamonds": self.raw_diamonds,
            "processed_diamonds": self.processed_diamonds
        })