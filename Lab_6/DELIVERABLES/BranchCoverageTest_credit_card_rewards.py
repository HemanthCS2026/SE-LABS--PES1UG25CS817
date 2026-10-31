
import pytest
from credit_card_rewards import (
    reward_points,
    late_payment_fee,
    card_status,
)


# Reward points tests

def test_classic_grocery():
    assert reward_points("classic", 1000, "grocery", False) == 10


def test_gold_grocery():
    assert reward_points("gold", 1000, "grocery", False) == 20


def test_platinum_grocery():
    assert reward_points("platinum", 1000, "grocery", False) == 40


def test_unknown_card_tier():
    with pytest.raises(ValueError, match="unknown card tier"):
        reward_points("silver", 1000, "grocery", False)


def test_invalid_amount_zero():
    with pytest.raises(ValueError, match="invalid amount"):
        reward_points("classic", 0, "grocery", False)


def test_invalid_amount_negative():
    with pytest.raises(ValueError, match="invalid amount"):
        reward_points("classic", -100, "grocery", False)


def test_fuel_category():
    assert reward_points("gold", 1000, "fuel", False) == 0


def test_dining_double_points():
    assert reward_points("classic", 1000, "dining", False) == 20


def test_travel_double_points():
    assert reward_points("gold", 1000, "travel", False) == 40


def test_weekend_bonus_gold():
    assert reward_points("gold", 1000, "grocery", True) == 70


def test_weekend_bonus_platinum():
    assert reward_points("platinum", 1000, "grocery", True) == 90


def test_classic_gets_no_weekend_bonus():
    assert reward_points("classic", 1000, "grocery", True) == 10


def test_other_category_no_multiplier():
    assert reward_points("classic", 1000, "shopping", False) == 10


def test_amount_below_100():
    assert reward_points("gold", 99, "grocery", False) == 0


# Late payment fee tests

def test_paid_on_time():
    assert late_payment_fee(5000, 0) == 0


def test_no_outstanding_balance():
    assert late_payment_fee(0, 10) == 0


def test_small_outstanding_fee():
    assert late_payment_fee(1000, 10) == 100


def test_medium_outstanding_fee():
    assert late_payment_fee(5000, 10) == 500


def test_large_outstanding_fee():
    assert late_payment_fee(15000, 10) == 1000


def test_fee_for_more_than_30_days_late():
    assert late_payment_fee(5000, 31) == 1250


def test_fee_at_exactly_30_days():
    assert late_payment_fee(5000, 30) == 500


def test_fee_at_10000_boundary():
    assert late_payment_fee(10000, 10) == 500


def test_fee_above_10000_boundary():
    assert late_payment_fee(10001, 10) == 1000


def test_negative_days_late():
    assert late_payment_fee(5000, -1) == 0


def test_negative_outstanding():
    assert late_payment_fee(-100, 10) == 0


# Card status tests

def test_frozen_card():
    assert card_status(50, 0, True) == "frozen"


def test_blocked_after_three_missed_payments():
    assert card_status(20, 3, False) == "blocked"


def test_blocked_after_more_than_three_missed_payments():
    assert card_status(20, 4, False) == "blocked"


def test_over_limit_risk():
    assert card_status(91, 0, False) == "over limit risk"


def test_exactly_90_percent_utilisation():
    assert card_status(90, 0, False) == "watch"


def test_watch_due_to_utilisation():
    assert card_status(50, 0, False) == "watch"


def test_watch_due_to_missed_payment():
    assert card_status(20, 1, False) == "watch"


def test_good_status():
    assert card_status(30, 0, False) == "good"


def test_good_status_at_zero_utilisation():
    assert card_status(0, 0, False) == "good"


def test_frozen_takes_priority():
    assert card_status(95, 4, True) == "frozen"
