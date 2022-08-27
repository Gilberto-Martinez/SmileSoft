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


from http.client import SWITCHING_PROTOCOLS


# dia = 4

# with SWITCHING_PROTOCOLS(dia) as s:
# 	if s.case(1, True):
# 		print('lunes')
# 	if s.case(2, True):
# 		print('martes')
# 	if s.case(3, True):
# 		print('miércoles')
# 	if s.case(4, True):
# 		print('jueves')
# 	if s.case(5, True):
# 		print('viernes')
# 	if s.case(6, True):
# 		print('sábado')
# 	if s.case(7, True):
# 		print('domingo')
# 	if s.default():
# 		print('error')


#<-->
# dia = 4

# with switch(dia) as s:
# 	if s.case(1):
# 		pass
# 	if s.case(2):
# 		pass
# 	if s.case(3):
# 		pass
# 	if s.case(4):
# 		pass
# 	if s.case(5, True):
# 		print('día de semana')
# 	if s.case(6):
# 		pass
# 	if s.case(7, True):
# 		print('fin de semana')
# 	if s.default():
# 		print('error')
