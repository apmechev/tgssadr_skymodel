from tempfile import NamedTemporaryFile
from tgss2bbs2 import  main 


def test_makes_a_skymodel_from_3Csource():
    with NamedTemporaryFile() as temp_file:
        main(srcID="3C48", radius=1, DoDec=True, output=temp_file.name)
        lines=[]
        for line in open(temp_file.name,'r').read().split('\n'):
            lines.append(line)
        assert lines[0] == "FORMAT = Name, Type, Patch, Ra, Dec, I, Q, U, V, MajorAxis, MinorAxis, Orientation, ReferenceFrequency='147500000.0', SpectralIndex='[]'"
        assert lines[2] ==" , , Patch, 01:37:41.2996, +33.09.35.079"
        for line in lines[3:-2]:
            assert "GAUSSIAN" in line or "POINT" in line
