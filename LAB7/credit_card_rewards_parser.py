"""Robust parsers for credit-card rewards input."""

def mask_card_number(number):
    """Mask a card number, preserving only its last four characters."""
    if not isinstance(number, str):
        return ""

    digits = "".join(ch for ch in number if ch.isalnum())
    if not digits:
        return ""

    return "*" * max(0, len(digits) - 4) + digits[-4:]


def parse_transaction(line):
    """Parse date, category and amount safely."""
    if not isinstance(line, str):
        return ("", 0)

    parts = line.split(",")
    if len(parts) != 3:
        return ("", 0)

    date, category, amount_text = (part.strip() for part in parts)

    if not date or not category or not amount_text:
        return ("", 0)

    try:
        amount = int(amount_text.replace(",", ""))
    except ValueError:
        return ("", 0)

    return (category.lower(), amount)


def parse_statement_total(text):
    """Parse a statement total safely."""
    if not isinstance(text, str) or ":" not in text:
        return 0

    _, amount_text = text.split(":", 1)
    amount_text = amount_text.strip().replace(",", "")

    if not amount_text:
        return 0

    try:
        return int(amount_text)
    except ValueError:
        return 0


def main():
    print("==== Running mask_card_number ====")
    value = input("Enter a card number (e.g. 4111 1111 1111 1234): ")
    print("Masked card number:", mask_card_number(value))

    print("\n==== Running parse_transaction ====")
    value = input(
        "Enter a transaction as DATE,CATEGORY,AMOUNT "
        "(e.g. 2026-11-05,dining,1550): "
    )
    print("Category and amount:", parse_transaction(value))

    print("\n==== Running parse_statement_total ====")
    value = input("Enter the statement total line (e.g. Total: 12,500): ")
    print("Statement total:", parse_statement_total(value))


if __name__ == "__main__":
    main()
