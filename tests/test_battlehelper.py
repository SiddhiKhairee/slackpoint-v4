from helpers.battlehelper import BattleHelper


###########################
# Test calculate_damage() #
###########################

def test_calculate_damage():
    """
    Tests whether the damage calculations are completely functional and return expected values
    """


def test_calculate_damage_high_defense():
    """
    Tests checks relating to damage calculations that end up being less than 1.
    They should all return 1 damage as the lowest possible value.
    """

    assert BattleHelper.calculate_damage(5, 0, 0, 5) >= 1, "Damage calculator should not be 1 or less if power is more than 1"


def test_calculate_damage_zero_boundary():
    """
    Tests boundary with the lowest possible damage calculation value, resulting in a negative denominator.
    This should return as 1 damage and is only possible of defense and power are both 0.
    """

    # Test damage calculations in all possible values of luck
    for i in range(0, 99):
        assert BattleHelper.calculate_damage(0, i, 0, 0) == 1, "Damage calculator did not calculate zero boundary correctly with Luck value of {}".format(i)
    
    # Test instances where power would not be zero, should return higher than 1
    assert BattleHelper.calculate_damage(5, 0, 0, 0) >= 1, "Damage calculator should not be 1 or less if power is more than 1"
    assert BattleHelper.calculate_damage(0, 0, 5, 0) >= 1, "Damage calculator should not be 1 or less if power is more than 1"


def test_calculate_damage_negative():
    """
    Tests negative values being used in the damage calculations. This may be useful to test if debuffs are
    added as a mechanic, which could induce negative values depending on the implementation.
    """


def test_calculate_damage_max_luck():
    """
    Tests damage calculation with maximum luck values, this should calculate values with very small random
    variation in damage calculation.
    """

#################################
# Test calculate_fixed_damage() #
#################################


def test_calculate_fixed_damage():
    """
    Tests whether the damage calculations are completely functional and return expected values
    """


def test_calculate_fixed_damage_high_defense():
    """
    Tests checks relating to damage calculations that end up being less than 1.
    They should all return 1 damage as the lowest possible value.
    """


def test_calculate_fixed_damage_zero_boundary():
    """
    Tests boundary with the lowest possible damage calculation value, resulting in a negative denominator.
    This should return as 1 damage.
    """


def test_calculate_fixed_damage_negative():
    """
    Tests negative values being used in the damage calculations. This may be useful to test if debuffs are
    added as a mechanic, which could induce negative values depending on the implementation.
    """

#############################
# Test calculate_hit_rate() #
#############################


def test_calculate_hit_rate():
    """
    Tests the hit rate calculation function using several different values
    """


def test_calculate_hit_rate_smallest():
    """
    Tests the smallest possible value for hit rate calculation (0.5 multiplier)
    """


def test_calculate_hit_rate_largest():
    """
    Tests the largest possible value for hit rate calculation (2.0 multiplier)
    """
