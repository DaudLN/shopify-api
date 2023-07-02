from django.utils.translation import ngettext


def get_message(model: str, count: int) -> str:
    return ngettext(
        "This collection can not be deleted as it contains %(count)d %(model)s",
        "This collection can not be deleted as it contains %(count)d %(model)ss",
        count,
    ) % {
        "count": count,
        "model": model,
    }
