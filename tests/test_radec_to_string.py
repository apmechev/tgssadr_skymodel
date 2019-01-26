from radec_to_string import radec_to_string
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
