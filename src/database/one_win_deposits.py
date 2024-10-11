from peewee import fn

from .models import OneWinDeposit



def get_user_deposits_summ(one_win_id: int) -> float:
    user_deposits_sum = (
        OneWinDeposit
        .select(fn.SUM(OneWinDeposit.amount))
        .where(OneWinDeposit.one_win_id == one_win_id)
        .scalar()
    )

    if not user_deposits_sum:
        return 0.0
    return user_deposits_sum
