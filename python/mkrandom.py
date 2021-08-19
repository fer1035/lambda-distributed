"""
Return random string.

return str
"""
import random
import string


def mkrandom(length: int, punctuations: bool = False) -> str:
    """
    Return random string.

    return str
    """
    if punctuations is True:
        response = ''.join(
            random.choices(
                string.ascii_lowercase +
                string.ascii_uppercase +
                string.digits +
                string.punctuation,
                k=length
            )
        )
    else:
        response = ''.join(
            random.choices(
                string.ascii_lowercase +
                string.ascii_uppercase +
                string.digits,
                k=length
            )
        )

    return response
