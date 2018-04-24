import settings


def sell(user_info, instrument_info):
    user_notes = user_info['portfolio'][0]['notes']  # amount ETH notes
    price = instrument_info['price'] + settings.PROCENT  # price for sale

    if user_notes > settings.NOTES_AMOUNT:
        return {
            'count': settings.NOTES_AMOUNT,
            'price': price,
        }
    elif user_notes:
        return {
            'count': user_notes,
            'price': price,
        }


def buy(user_info, instrument_info):
    user_wmz = user_info['balance']['wmz']  # amount WMZ
    price = instrument_info['price'] - settings.PROCENT  # price for buy

    if user_wmz >= settings.NOTES_AMOUNT * price:
        return {
            'count': settings.NOTES_AMOUNT,
            'price': price,
        }
    elif user_wmz >= price:
        return {
            'count': int(user_wmz/price),
            'price': price,
        }
