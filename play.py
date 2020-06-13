import locale
import datetime

dt = datetime.datetime(2015, 11, 15, 16, 30)

# locale.setlocale(locale.LC_ALL, "en_GB.utf8")
# print(dt.strftime("%A, %d. %B %Y %I:%M%p"))

locale.setlocale(locale.LC_TIME, "bn_bd")
print(dt.strftime("%A, %d. %B %Y %I:%M%p"))