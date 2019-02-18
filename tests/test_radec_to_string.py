from radec_to_string import radec_to_string
from radec_to_string import degdeg_to_hmsdms
import random

def test_zero_is_360():
    assert(radec_to_string([360,0]) == radec_to_string([0,0]))
    for multiplier in range(1,10):
        assert(radec_to_string([360 * multiplier,0]) ==
                radec_to_string([0,0]))

def test_dec_over_90():
    assert(radec_to_string([0,91]) == radec_to_string([0,89]))
    assert(radec_to_string([0,99]) == radec_to_string([0,81]))
    for _ in range(1,10):
        rand_dec = random.uniform(0,90)
        assert(radec_to_string([0,90-rand_dec]) == radec_to_string([0, 90 + rand_dec]))

def test_output():
    result = '00h00m00.0000s +89d00\'00.000"'
    assert(result == radec_to_string([0,89]))

def test_decimals():
    assert(radec_to_string([0,0],decimals=[0,0]) == '00h00m00s +00d00\'00"')
    assert(radec_to_string([0,0],decimals=[1,1]) == '00h00m00.0s +00d00\'00.0"')
    assert(radec_to_string([0,0],decimals=[5,5]) == '00h00m00.00000s +00d00\'00.00000"')

def test_precisions():
    assert(degdeg_to_hmsdms([0,0],[0]) == [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    assert(degdeg_to_hmsdms([0,0],0) == [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    assert(degdeg_to_hmsdms([0,0],[0,1]) == [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

