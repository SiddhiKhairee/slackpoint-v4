
class Move:
    """
    A move that players can use against each other.

    :name: The name of the move
    :description: The description of the move that tells the player what it does
    :move_type: The type of move it is (Physical, Magic, Healing, etc.)
    :base_power: The amount of power that the Move has
    :base_hit_rate: The base accuracy of the Move
    :mp_cost: The amount of MP that the move costs
    :hp_percent_cost: The percentage of HP that the move will cost
    """

    def __init__(self, name: str, description: str, move_type: str, base_power: int,
                 base_hit_rate: int, mp_cost: int, hp_percent_cost: float):
        """
        Initializes a Move with all of its necessary components for damage calculation
        """

        self.name = name
        self.description = description
        self.move_type = move_type
        self.base_power = base_power
        self.base_hit_rate = base_hit_rate
        self.mp_cost = mp_cost
        self.hp_percent_cost = hp_percent_cost
