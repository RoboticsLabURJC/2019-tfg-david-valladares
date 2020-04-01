# -*- coding: utf-8 -*-

from datetime import tzinfo, timedelta, datetime

class ColorPrint():
    ''' Clase con las claves de todos los colores disponible para pintar en la consola. 
        USO => ColorPrint.COLOR + str + ColorPrint.END '''

    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Define UTC Timezone for Python 2.x
ZERO = timedelta(0)

class UTC(tzinfo):
  def utcoffset(self, dt):
    return ZERO
  def tzname(self, dt):
    return "UTC"
  def dst(self, dt):
    return ZERO
