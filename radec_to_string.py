###############################################################################

from numpy import *
from math import atan2
###############################################################################

def radec_to_string( radec, decimals = [ 4, 3 ], do_iau = False,
    separators = [ 'h', 'm', 's ', 'd', "'", '"' ] ):
  hmsdms = degdeg_to_hmsdms( radec )
  [ a, b ] = decimals
  if do_iau:
    x = 4
    a = a + x
    b = b + x
  format = '%02d' + separators[ 0 ] + '%02d' + separators[ 1 ] + '%0'
  if ( a > 0 ):
    format = format + repr( 3 + a ) + '.' +  repr( a ) + 'f' + separators[ 2 ]
  else:
    format = format + '2d' + separators[ 2 ]
  string = format % ( hmsdms[ 0 ], hmsdms[ 1 ], hmsdms[ 2 ] )
  if ( asign( hmsdms[ 3 ] ) < 0. ):
    string = string + '-'
    hmsdms[ 3 ] = -hmsdms[ 3 ]
  else:
    string = string + '+'
  format = '%02d' + separators[ 3 ] + '%02d' + separators[ 4 ] + '%0'
  if ( b > 0 ):
    format = format + repr( 3 + b ) + '.' + repr( b ) + 'f' + separators[ 5 ]
  else:
    format = format + '2d' + separators[ 5 ]
  string = string + format % ( hmsdms[ 3 ], hmsdms[ 4 ], hmsdms[ 5 ] )
  if do_iau:
    try:
      index1 = string.index( '+' ) - len( separators[ 2 ] ) - x
    except ValueError:    
      index1 = string.index( '-' ) - len( separators[ 2 ] ) - x
    index2 = len( string ) - len( separators[ 5 ] ) - 4
    string = string[ : index1 ] + string[ index1 + x : index2 ] + string[ index2 + x : ]
    if ( decimals[ 0 ] == 0 ):
      string = string[ : index1 - 1 ] + string[ index1 : ]
    if ( decimals[ 1 ] == 0 ):
      index2 = len( string ) - len( separators[ 5 ] )
      string = string[ : index2 - 1 ] + string[ index2 : ]
  return string

###############################################################################

def degdeg_to_hmsdms( degdeg, precision = None ):
  ra_deg = amodulo( degdeg[ 0 ], 360. )
  ra_h = floor( ra_deg / 15. )
  ra_m = floor( 60. * ( ( ra_deg / 15. ) - ra_h ) )
  ra_s = 3600. * ( ( ra_deg / 15. ) - ra_h - ( ra_m / 60. ) )
  dec_deg = asign( degdeg[ 1 ] ) * degrees( math.asin( 
      max( - 1., min( 1., sin( radians( amodulo( fabs( degdeg[ 1 ] ), 360. ) ) ) ) ) ) )
  dec_d = asign( dec_deg ) * floor( abs( dec_deg ) )
  dec_m = floor( 60. * abs( dec_deg - dec_d ) )
  dec_s = 3600. * ( abs( dec_deg - dec_d ) - ( dec_m / 60. ) )
  if ( not precision is None ):
    if ( len( shape( precision ) ) == 0 ):
      prec1 = int( precision )
      prec2 = int( precision )
    elif ( len( precision ) == 1 ):
      prec1 = int( precision[ 0 ] )
      prec2 = int( precision[ 0 ] )
    else:
      prec1 = int( precision[ 0 ] )
      prec2 = int( precision[ 1 ] )
    ra_s = around( ra_s, decimals = prec1 )
    dec_s = around( dec_s, decimals = prec2 )
  if ( ra_s >= 60. ):
    ra_s = ra_s - 60.
    ra_m = ra_m + 1.
  if ( ra_m >= 60. ):
    ra_m = ra_m - 60.
    ra_h = ra_h + 1.
  if ( ra_h >= 24. ):
    ra_h = ra_h - 24.
  if ( dec_s >= 60. ):
    dec_s = dec_s - 60.
    dec_m = dec_m + 1.
  if ( dec_m >= 60. ):
    dec_m = dec_m - 60.
    if ( asign( dec_deg ) > 0. ):
      dec_d = dec_d + 1.
      if ( dec_d == 90. ):
        dec_s = 0.
        dec_m = 0.
    else:
      dec_d = dec_d - 1.
      if ( dec_d == - 90. ):
        dec_s = 0.
        dec_m = 0.
  return [ ra_h, ra_m, ra_s, dec_d, dec_m, dec_s ]

###############################################################################

def amodulo( x, y ):
  if ( not is_array( x ) ):
    if ( not is_array( y ) ):
      m = x - y * floor( x / ( y + float( y == 0. ) ) )
    else:
      xx = x * aones( y )
      m = xx - y * floor( x / ( y + array( y == 0., dtype = y.dtype ) ) )
  else:
    if ( not is_array( y ) ):
      yy = y * aones( x )
      m = x - yy * floor( x / ( yy + array( yy == 0., dtype = yy.dtype ) ) )
    else:
      m = x - y * floor( x / ( y + array( y == 0., dtype = y.dtype ) ) )
  return m

###############################################################################

def is_array( a ):
  return isinstance( a, type( array( [ 1 ] ) ) )

###############################################################################

def aones( x ):
  if ( len( x.shape ) == 0 ):
    one = 1.
  else:
    one = ones( shape = x.shape, dtype = x.dtype )
  return one

###############################################################################

def asign( x ):
# this function also separates between -0 and +0
  if ( not is_array( x ) ):
    s = ( - 2. * float( aatan2( x, x ) < 0. ) + 1. )
  else:
    s = ( - 2. * array( aatan2( x, x ) < 0., dtype = x.dtype ) + 1. )
  return s

###############################################################################

def aatan2( y, x ):
  if ( shape( x ) != shape( y ) ):
    raise error( 'x and y have different shapes' )
  if ( len( shape( x ) ) == 0 ):
    z = atan2( y, x )
  else:
    xx = x.ravel()
    yy = y.ravel()
    zz = array( [ atan2( yy[ i ], xx[ i ] ) for i in range( len( xx ) ) ], dtype = x.dtype )
    z = zz.reshape( x.shape )
  return z

###############################################################################

