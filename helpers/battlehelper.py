from random import uniform
from math import floor, ceil


class BattleHelper:
    """
    A calculator class that contains functions that are able to calculate damage and hit rate values for battle.
    """

    @staticmethod
    def calculate_damage(user_atk: int, user_luk: int, move_power: int, target_def: int) -> int:
        """
        Calculates the damage based on the inputted values for attack, move power, and defense. This function
        is meant to be customizable in that the attack type and defense types can be varied to create a variety 
        of different attack variations.

        (e.g. Physical, Magical, Physical that hits Resistance, Magical that hits Defense)

        :param user_atk: The value associated with the player's attack stat (STR, MAG, etc.)
        :param user_luk: The amount of luck the user has, make random factor roll higher
        :param move_power: The value representative of the power of the move being used
        :param target_def: The defense value used to dampen the amount of damage being dealt
        :type user_atk: int
        :type user_luk: int
        :type move_power: int
        :type target_def: int
        :rtype: int
        """

        # The amount of total power the user's attack and move power creates
        power = move_power + (2 * user_atk)

        # Calculate the amount of damage based on the target's defense
        damage = power**2 / (power - (5 * target_def))

        # Generate random multiplier value (less variation the more Luck the user has)
        rng_roll = uniform(1.0 + (user_luk / 100), 1.1)

        return floor(rng_roll * damage)

    @staticmethod
    def calculate_hit_rate(user_agl: int, user_luk: int, move_hit: int, target_agl: int, target_luk: int) -> int:
        """
        Calculate the hit rates and dodging capabilities of each of the parties involved. The agility and luck values 
        are used for the calculation of the hit rate multiplier, which is made to modify the hit rate of the move.

        :param user_agl: The user's agility stat, used in hit calculations
        :param user_luk: The user's luck stat, used moderately in hit calculations
        :param move_hit: The base hit chance value of a move
        :param target_agl: The target's agility stat, used in evasion calculations
        :param target_luk: The target's luck stat, used in evasion calculations to a lesser extent
        :type user_agl: int
        :type user_luk: int
        :type move_hit: int
        :type target_agl: int
        :type target_luk: int
        :rtype: int
        """

        # Defines hit rate and dodge values for each of two involved parties and uses them to calculate the hit rate multiplier
        user_hit_val = user_agl + (user_luk * 0.3) + 128.7
        target_hit_val = target_agl + (target_luk * 0.3) + 128.7
        hit_rate_multplier = user_hit_val / target_hit_val

        # Calculate hit rate
        hit_rate = hit_rate_multplier * move_hit
        return ceil(hit_rate)
