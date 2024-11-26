from helpers.battlehelper import BattleHelper


###########################
# Test calculate_damage() #
###########################


def test_calculate_damage():
    """
    Tests whether the damage calculations are completely functional and return expected values
    """

    # Check to see if BattleHelper calculates values that fall within the range of the random generation 50 times
    for i in range(0, 50):
        damage = BattleHelper.calculate_damage(46, 0, 80, 22)
        assert damage >= 104 and damage <= 115, "Test higher move power than atk"

    for i in range(0, 50):
        damage = BattleHelper.calculate_damage(73, 0, 20, 60)
        assert damage >= 59 and damage <= 65, "Test higher atk than move power"

    for i in range(0, 50):
        damage = BattleHelper.calculate_damage(99, 50, 200, 43)
        assert (
            damage >= 271 and damage <= 284
        ), "50 luck test reduces RNG variance by 0.05"


def test_calculate_damage_high_defense():
    """
    Tests checks relating to damage calculations that end up being less than 1.
    They should all return 1 damage as the lowest possible value.
    """

    # Test using different amounts of base powers against a very large defense value that should do 1 damage
    assert (
        BattleHelper.calculate_damage(5, 0, 0, 200) == 1
    ), "Damage calculator should return as 1 if the value calculated becomes negative."
    assert (
        BattleHelper.calculate_damage(0, 0, 5, 200) == 1
    ), "Damage calculator should return as 1 if the value calculated becomes negative."
    assert (
        BattleHelper.calculate_damage(5, 0, 5, 200) == 1
    ), "Damage calculator should return as 1 if the value calculated becomes negative."

    # Test using different amounts of base powers with maximum Luck
    assert (
        BattleHelper.calculate_damage(5, 99, 0, 200) == 1
    ), "Damage calculator should return as 1 if the value calculated becomes negative, even with max Luck."
    assert (
        BattleHelper.calculate_damage(0, 99, 5, 200) == 1
    ), "Damage calculator should return as 1 if the value calculated becomes negative, even with max Luck."
    assert (
        BattleHelper.calculate_damage(5, 99, 5, 200) == 1
    ), "Damage calculator should return as 1 if the value calculated becomes negative, even with max Luck."


def test_calculate_damage_zero_boundary():
    """
    Tests boundary with the lowest possible damage calculation value, resulting in a negative denominator.
    This should return as 1 damage and is only possible of defense and power are both 0.
    """

    # Test damage calculations in all possible values of luck
    for i in range(0, 99):
        assert (
            BattleHelper.calculate_damage(0, i, 0, 0) == 1
        ), "Damage calculator did not calculate zero boundary correctly with Luck value of {}".format(
            i
        )

    # Test instances where power would not be zero, should return higher than 1
    assert (
        BattleHelper.calculate_damage(5, 0, 0, 0) >= 1
    ), "Damage calculator should not be 1 or less if power is more than 1"
    assert (
        BattleHelper.calculate_damage(0, 0, 5, 0) >= 1
    ), "Damage calculator should not be 1 or less if power is more than 1"


def test_calculate_damage_negative():
    """
    Tests negative values being used in the damage calculations. This may be useful to test if debuffs are
    added as a mechanic, which could induce negative values depending on the implementation.
    """

    # Test with negative offensive values
    assert (
        BattleHelper.calculate_damage(-5, 0, 0, 0) == 1
    ), "Damage calculator should be 1 if damage is negative"
    assert (
        BattleHelper.calculate_damage(0, 0, -5, 0) == 1
    ), "Damage calculator should be 1 if damage is negative"
    assert (
        BattleHelper.calculate_damage(-5, 0, -5, 0) == 1
    ), "Damage calculator should be 1 if damage is negative"

    # Test with negative defensive values and positive attack values
    damage = BattleHelper.calculate_damage(5, 0, 5, -5)
    assert (
        damage >= 22 and damage <= 25
    ), "Damage should be between 22-25 with 10 atk and -5 def"

    # Test with negative defense and attack values
    damage = BattleHelper.calculate_damage(-5, 0, -5, -5)
    assert damage == 1, "Damage should be 1 since power is set to 0 when negative"


def test_calculate_damage_max_luck():
    """
    Tests damage calculation with maximum luck values, this should calculate values with very small random
    variation in damage calculation.
    """

    # Check to see if BattleHelper calculates values that fall within the range of the random generation 50 times
    for i in range(0, 50):
        damage = BattleHelper.calculate_damage(46, 99, 80, 22)
        assert (
            damage == 115
        ), "Test higher move power than atk; the variance is low enough to make it floor to 115 every time"

    for i in range(0, 50):
        damage = BattleHelper.calculate_damage(73, 99, 20, 60)
        assert (
            damage >= 64 and damage <= 65
        ), "Test higher atk than move power, should be between 64-65"

    for i in range(0, 50):
        damage = BattleHelper.calculate_damage(99, 99, 200, 43)
        assert (
            damage >= 283 and damage <= 284
        ), "Test very high values, should be between 283-284"


def test_calculate_damage_overload_luck():
    """
    Tests damage calculation with over maximum luck values, this should calculate values with very small random
    variation in damage calculation, but should not exceed a minimum of a multiplier of 1.099 since the luck should
    be set to 99 at the max.
    """

    # Check to see if BattleHelper calculates values that fall within the range of the random generation 50 times despite overloaded luck
    for i in range(0, 50):
        damage = BattleHelper.calculate_damage(46, 200, 80, 22)
        assert (
            damage == 115
        ), "Test higher move power than atk; the variance is low enough to make it floor to 115 every time"

    for i in range(0, 50):
        damage = BattleHelper.calculate_damage(73, 500, 20, 60)
        assert (
            damage >= 64 and damage <= 65
        ), "Test higher atk than move power, should be between 64-65"

    for i in range(0, 50):
        damage = BattleHelper.calculate_damage(99, 9999999, 200, 43)
        assert (
            damage >= 283 and damage <= 284
        ), "Test very high values, should be between 283-284"


#################################
# Test calculate_fixed_damage() #
#################################


def test_calculate_fixed_damage():
    """
    Tests whether the damage calculations are completely functional and return expected values
    """

    # Check to see if BattleHelper calculates values that DO NOT have variance
    for i in range(0, 50):
        damage = BattleHelper.calculate_fixed_damage(46, 80, 22)
        assert damage == 104, "Test higher move power than atk"

    for i in range(0, 50):
        damage = BattleHelper.calculate_fixed_damage(73, 20, 60)
        assert damage == 59, "Test higher atk than move power"

    for i in range(0, 50):
        damage = BattleHelper.calculate_fixed_damage(99, 200, 43)
        assert damage == 258, "Test very high attack power"


def test_calculate_fixed_damage_high_defense():
    """
    Tests checks relating to damage calculations that end up being less than 1.
    They should all return 1 damage as the lowest possible value.
    """

    # Test using different amounts of base powers against a very large defense value that should do 1 damage
    assert (
        BattleHelper.calculate_fixed_damage(5, 0, 200) == 1
    ), "Damage calculator should return as 1 if the value calculated becomes negative."
    assert (
        BattleHelper.calculate_fixed_damage(0, 5, 200) == 1
    ), "Damage calculator should return as 1 if the value calculated becomes negative."
    assert (
        BattleHelper.calculate_fixed_damage(5, 5, 200) == 1
    ), "Damage calculator should return as 1 if the value calculated becomes negative."


def test_calculate_fixed_damage_zero_boundary():
    """
    Tests boundary with the lowest possible damage calculation value, resulting in a negative denominator.
    This should return as 1 damage.
    """

    assert (
        BattleHelper.calculate_fixed_damage(0, 0, 0) == 1
    ), "Damage calculator did not calculate zero boundary correctly if it divides by 0"

    # Test instances where power would not be zero, should return higher than 1
    assert (
        BattleHelper.calculate_fixed_damage(5, 0, 0) >= 1
    ), "Damage calculator should not be 1 or less if power is more than 1"
    assert (
        BattleHelper.calculate_fixed_damage(0, 5, 0) >= 1
    ), "Damage calculator should not be 1 or less if power is more than 1"


def test_calculate_fixed_damage_negative():
    """
    Tests negative values being used in the damage calculations. This may be useful to test if debuffs are
    added as a mechanic, which could induce negative values depending on the implementation.
    """

    # Test with negative offensive values
    assert (
        BattleHelper.calculate_fixed_damage(-5, 0, 0) == 1
    ), "Damage calculator should be 1 if damage is negative"
    assert (
        BattleHelper.calculate_fixed_damage(0, -5, 0) == 1
    ), "Damage calculator should be 1 if damage is negative"
    assert (
        BattleHelper.calculate_fixed_damage(-5, -5, 0) == 1
    ), "Damage calculator should be 1 if damage is negative"

    # Test with negative defensive values and positive attack values
    damage = BattleHelper.calculate_fixed_damage(5, 5, -5)
    assert (
        damage == 22
    ), "Damage should be 23 with 10 atk and -5 def, no variance observed"

    # Test with negative defense and attack values
    damage = BattleHelper.calculate_fixed_damage(-5, -5, -5)
    assert damage == 1, "Damage should be 1 since power is set to 0 when negative"


#############################
# Test calculate_hit_rate() #
#############################


def test_calculate_hit_rate():
    """
    Tests the hit rate calculation function using several different values
    """

    # Calculate hit rates with varying positive base stat values from 0-99 (normal functionality)
    assert (
        BattleHelper.calculate_hit_rate(15, 50, 70, 20, 90) == 64
    ), "Values tested should match values that are in the model, always rounded up"
    assert (
        BattleHelper.calculate_hit_rate(27, 45, 80, 56, 25) == 71
    ), "Values tested should match values that are in the model, always rounded up"
    assert (
        BattleHelper.calculate_hit_rate(47, 86, 40, 37, 65) == 44
    ), "Values tested should match values that are in the model, always rounded up"
    assert (
        BattleHelper.calculate_hit_rate(69, 23, 90, 47, 75) == 93
    ), "Values tested should match values that are in the model, always rounded up"
    assert (
        BattleHelper.calculate_hit_rate(1, 90, 20, 78, 1) == 16
    ), "Values tested should match values that are in the model, always rounded up"


def test_calculate_hit_rate_same_stats():
    """
    Tests the hit rate calculation function using values that match from both user and target. This should cause the multiplier
    to be exactly 1.0 for the hit rate, meaning that it should match the move's base hit rate value.
    """

    # Calculate hit rates with same stats
    assert (
        BattleHelper.calculate_hit_rate(0, 0, 0, 0, 0) == 0
    ), "Should multiply hit rate by 1 if stat totals match"
    assert (
        BattleHelper.calculate_hit_rate(0, 0, 80, 0, 0) == 80
    ), "Should multiply hit rate by 1 if stat totals match"
    assert (
        BattleHelper.calculate_hit_rate(20, 0, 80, 20, 0) == 80
    ), "Should multiply hit rate by 1 if stat totals match"
    assert (
        BattleHelper.calculate_hit_rate(0, 30, 80, 0, 30) == 80
    ), "Should multiply hit rate by 1 if stat totals match"
    assert (
        BattleHelper.calculate_hit_rate(40, 40, 80, 40, 40) == 80
    ), "Should multiply hit rate by 1 if stat totals match"


def test_calculate_hit_rate_same_stat_total():
    """
    Tests the hit rate calculation function using values that do not match between user and target. When calculated, however,
    these values should add up to the same accuracy values used for the numerator and denominator, making the multiplier 1.0.
    This causes the result to be the same as the base hit rate.
    """

    # Calculate hit rates with same accuracy stat totals
    assert (
        BattleHelper.calculate_hit_rate(59, 30, 80, 50, 60) == 80
    ), "Should multiply hit rate by 1 if stat totals match"
    assert (
        BattleHelper.calculate_hit_rate(50, 60, 80, 59, 30) == 80
    ), "Should multiply hit rate by 1 if stat totals match"
    assert (
        BattleHelper.calculate_hit_rate(69, 20, 80, 48, 90) == 80
    ), "Should multiply hit rate by 1 if stat totals match"
    assert (
        BattleHelper.calculate_hit_rate(48, 90, 80, 69, 20) == 80
    ), "Should multiply hit rate by 1 if stat totals match"


def test_calculate_hit_rate_smallest():
    """
    Tests the smallest possible value for hit rate calculation using min base stats (0.5 multiplier)
    """

    # Calculate the smallest possible hit rates for a multitude of base hit rates
    assert (
        BattleHelper.calculate_hit_rate(0, 0, 100, 99, 99) == 50
    ), "Get the max difference between base stats should halve base hit rate if target has max stats and user doesn't"
    assert (
        BattleHelper.calculate_hit_rate(0, 0, 80, 99, 99) == 40
    ), "Get the max difference between base stats should halve base hit rate if target has max stats and user doesn't"
    assert (
        BattleHelper.calculate_hit_rate(0, 0, 60, 99, 99) == 30
    ), "Get the max difference between base stats should halve base hit rate if target has max stats and user doesn't"
    assert (
        BattleHelper.calculate_hit_rate(0, 0, 40, 99, 99) == 20
    ), "Get the max difference between base stats should halve base hit rate if target has max stats and user doesn't"
    assert (
        BattleHelper.calculate_hit_rate(0, 0, 20, 99, 99) == 10
    ), "Get the max difference between base stats should halve base hit rate if target has max stats and user doesn't"


def test_calculate_hit_rate_largest():
    """
    Tests the largest possible value for hit rate calculation using max base stats (2.0 multiplier)
    """

    # Calculates the largest possible hit rates for a multitude of base hit rates
    assert (
        BattleHelper.calculate_hit_rate(99, 99, 100, 0, 0) == 200
    ), "Getting the max difference between base stats should double base hit rate"
    assert (
        BattleHelper.calculate_hit_rate(99, 99, 80, 0, 0) == 160
    ), "Getting the max difference between base stats should double base hit rate"
    assert (
        BattleHelper.calculate_hit_rate(99, 99, 60, 0, 0) == 120
    ), "Getting the max difference between base stats should double base hit rate"
    assert (
        BattleHelper.calculate_hit_rate(99, 99, 40, 0, 0) == 80
    ), "Getting the max difference between base stats should double base hit rate"
    assert (
        BattleHelper.calculate_hit_rate(99, 99, 20, 0, 0) == 40
    ), "Getting the max difference between base stats should double base hit rate"


def test_calculate_hit_rate_zero_boundary():
    """
    Tests the zero boundary for the hit rate calculation. This should exist only at -99 AGL and LUK
    on the target side since it would cause the denominator at 0.
    """

    # Take care of denominator equaling 0; number should be very high if using normal values
    assert (
        BattleHelper.calculate_hit_rate(-99, -99, 80, -99, -99) == 0
    ), "-99 target AGL and LUK sets denominator to 1, and not error"
    assert (
        BattleHelper.calculate_hit_rate(50, 50, 80, -99, -99) == 15496
    ), "-99 target AGL and LUK sets denominator to 1, and not error"


def test_calculate_hit_rate_negative():
    """
    Tests the input of negative values into the hit rate calculation. A negative hit rate
    should, all things considered, make the move miss regardless, but the function will
    support negative values in the event that a future game mechanic utilizes it.
    """

    # Calculate with absolute minimum negative stats (-99 in AGL and LUK), should always equal 0 no matter what the opponent has
    assert (
        BattleHelper.calculate_hit_rate(-99, -99, 80, 0, 0) == 0
    ), "-99 user AGL and LUK should always return 0"
    assert (
        BattleHelper.calculate_hit_rate(-99, -99, 80, 99, 99) == 0
    ), "-99 user AGL and LUK should always return 0"
    assert BattleHelper.calculate_hit_rate(
        -99, -99, 80, 0, 0
    ) == BattleHelper.calculate_hit_rate(
        -99, -99, 80, 99, 99
    ), "-99 user AGL and LUK should always return 0"


def test_calculate_hit_rate_negative_hard_boundary():
    """
    Tests the input of negative values into the hit rate calculation. A negative hit rate
    should, all things considered, make the move miss regardless, but the function will
    support negative values in the event that a future game mechanic utilizes it.
    """

    # Calculate with over minimum negative stats (-99 in AGL and LUK), these should cap out at -99 as that is where it becomes undefined
    assert (
        BattleHelper.calculate_hit_rate(-99, -99, 80, -999, -999) == 0
    ), "-99 target AGL and LUK sets denominator to 1, and not error"
    assert BattleHelper.calculate_hit_rate(
        -99, -99, 80, -99, -99
    ) == BattleHelper.calculate_hit_rate(
        -99, -99, 80, -999, -999
    ), "-99 target AGL and LUK sets denominator to 1, and not error"
    assert (
        BattleHelper.calculate_hit_rate(50, 50, 80, -999, -999) == 15496
    ), "-99 target AGL and LUK sets denominator to 1, and not error"
    assert BattleHelper.calculate_hit_rate(
        50, 50, 80, -999, -999
    ) == BattleHelper.calculate_hit_rate(
        50, 50, 80, -99, -99
    ), "-99 target AGL and LUK sets denominator to 1, and not error"


def test_calculate_hit_rate_guaranteed():
    """
    Tests that the hit rate returned from a move with 101 accuracy or higher is labeled
    as a "true hit" move. In other words, it will never miss no matter what values are
    input.
    """

    assert (
        BattleHelper.calculate_hit_rate(0, 0, 101, 0, 0) == 100
    ), "Always return 100 if base hit rate is over 100"
    assert (
        BattleHelper.calculate_hit_rate(0, 0, 101, 99, 99) == 100
    ), "Always return 100 if base hit rate is over 100, this usually returns ~50"
    assert (
        BattleHelper.calculate_hit_rate(99, 99, 101, 0, 0) == 100
    ), "Always return 100 if base hit rate is over 100, this would return 202"
    assert (
        BattleHelper.calculate_hit_rate(-9, -9, 101, 0, 0) == 100
    ), "Always return 100 if base hit rate is over 100"
