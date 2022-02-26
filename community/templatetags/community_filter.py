import markdown
from django import template
from datetime import datetime
import math
from django.utils.safestring import mark_safe

register = template.Library()


# https://python-markdown.github.io/extensions/
@register.filter()
def mark(value):
    '''
    apply markdown for post content
    '''
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))


@register.filter()
def elapse_date(value):
    '''
    time elapsed from user's written time
    '''
    curTime = datetime.today()
    diffTime = curTime - value  # timedelta ( * days, HH:MM:SS )
    totalSeconds = int(diffTime.total_seconds())

    elapseMinute = math.floor(totalSeconds/60)
    if elapseMinute < 1:
        return "방금 전"
    elif elapseMinute < 60:
        return str(elapseMinute) + "분 전"

    elapseHour = math.floor(elapseMinute/60)
    if elapseHour < 24:
        return str(elapseHour) + "시간 전"

    elapseDay = math.floor(elapseHour/24)
    if elapseDay < 365:
        return str(elapseDay) + "일 전"

    return str(math.floor(elapseDay/365)) + "년 전"

@register.filter()
def post_type(value):

    if value == "developer":
        return "개발자"
    elif value == "free":
        return "자유"
    elif value == "bug":
        return "버그"
