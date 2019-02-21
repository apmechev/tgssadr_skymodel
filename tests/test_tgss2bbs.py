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

def test_name_and_coord_equals():
    coords = "24.42208167, 33.15974417"
    name = "3C48"
    with NamedTemporaryFile() as name_model:
        with NamedTemporaryFile() as coords_model:
            main(srcID=name, radius=1, DoDec=True, output=name_model.name)
            main(srcID=coords, radius=1, DoDec=True, output=coords_model.name)
            with open(name_model.name,'r') as _f:
                name_data = _f.read().split('\n')
                line_count_name = len(name_data)
            with open(coords_model.name,'r') as _f:
                coord_data = _f.read().split('\n')
                line_count_coord = len(coord_data)
            assert line_count_name == line_count_coord

            for line_n, line_c in zip(name_data, coord_data):
                assert line_n == line_c


