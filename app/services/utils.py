from datetime import datetime


def date_fr_vers_iso(date_fr):

    if not date_fr:
        return None

    date_fr = str(date_fr).strip()

    if date_fr == "":
        return None

    return datetime.strptime(
        date_fr,
        "%d/%m/%Y"
    ).strftime(
        "%Y-%m-%d"
    )