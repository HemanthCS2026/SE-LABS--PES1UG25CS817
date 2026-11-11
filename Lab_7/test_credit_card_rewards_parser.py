from hypothesis import given, strategies as st

from credit_card_rewards_parser import (
    mask_card_number,
    parse_transaction,
    parse_statement_total,
)


@given(st.text() | st.none())
def test_mask_card_number_no_crash(s):
    try:
        result = mask_card_number(s)
    except Exception as e:
        assert False, f"mask_card_number crashed with {s!r}: {e}"
    assert isinstance(result, str)


@given(st.text() | st.none())
def test_parse_transaction_no_crash(s):
    try:
        result = parse_transaction(s)
    except Exception as e:
        assert False, f"parse_transaction crashed with {s!r}: {e}"
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], str)
    assert isinstance(result[1], int)


@given(st.text() | st.none())
def test_parse_statement_total_no_crash(s):
    try:
        result = parse_statement_total(s)
    except Exception as e:
        assert False, f"parse_statement_total crashed with {s!r}: {e}"
    assert isinstance(result, int)
