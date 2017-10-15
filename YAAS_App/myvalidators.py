from datetime import datetime,timedelta

from django.core.exceptions import ValidationError


# def validate_endtime(endate):
#     print(endate)
#
#     if (datetime.strftime(endate, '%Y-%m-%d %H:%M')-datetime.now())<timedelta(hours=72):
#         raise ValidationError(('%endate) pidding time must be longer than 72 hours'),
#                               params={'endate':endate},)

#def validate_minpid(value):
