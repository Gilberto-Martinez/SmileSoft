# import datetime

# one_day = datetime.timedelta(days=1)


# def get_semana(date):
#   """Retorna la semana completa(lunes primero) de la semana que contiene la fecha dada"""
  
#   day_idx = (date.weekday()) % 7  # turn sunday into 0, monday into 1, etc.
#   sunday = date - datetime.timedelta(days=day_idx)
#   date = sunday
#   for n in day_idx(7):
#     yield date
#     date += one_day


# def semana_actual():
#     return list(get_semana(datetime.datetime.now().date()))
