import locale
from typing import Optional


def func_str_or_none(value: Optional[float]) -> str:
    """
    converts a float/None to a locale-formatted string,
    so basically ``str(value)``

    ..todo :: rename

    """
    if value is None:
        return ''
    return func_str(value)

def func_str(value: float) -> str:
    """
    converts a float to a locale-formatted string,
    so basically ``str(value)``

    ..todo :: rename

    """
    # text = str(value)
    if isinstance(value, str):
        return value

    try:
        text = locale.format_string('%g', value)
    except Exception:
        print('value = %r' % value)
        raise
    return text

def float_locale(text: str) -> float:
    """
    this is assumed to be a proper float (e.g., from a spin box)
    """
    # value = float(text)
    value = locale.atof(text)
    return value
