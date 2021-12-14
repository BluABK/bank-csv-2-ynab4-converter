import collections.abc


def update_nested_dict(d, u):
    """
    Recursively updates a nested dict (as dict.update() only works on non-nested structures).
    :param d: Dict to update.
    :param u: Dict with updated entries.
    :return:  Updated dict
    """
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update_nested_dict(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def currency2float(s):
    """
    Takes a currency amount string and returns a computed float value.

    NB: If Unicode parsing is required in future replace the reverser with this grapheme based solution:
    https://stackoverflow.com/a/56282726
    :param s:
    :return:
    """
    past_delim = False
    is_negative = False
    characteristic_str_rev = ''
    mantissa_str_rev = ''

    # Read every char from end to start so that the order is mantissa --> delim --> characteristic --> whether negative
    for c in s[::-1]:
        if c.isdigit():
            if not past_delim:
                mantissa_str_rev += c
            else:
                characteristic_str_rev += c
        elif c == '-':
            is_negative = True
        else:
            # Delim can be ',', '.', ' ' or anything not a digit depending on your locale.
            past_delim = True

    # Undo reversion of characteristic and mantissa
    characteristic_str = "".join(characteristic_str_rev[::-1])
    mantissa_str = "".join(mantissa_str_rev[::-1])

    return float(('-' if is_negative else '') + characteristic_str + '.' + mantissa_str)
