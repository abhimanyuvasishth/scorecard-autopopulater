from scorecard_autopopulater.utils import get_letters, num_2_str, str_2_num


def test_column_number_conversion():
    assert num_2_str(str_2_num('A')) == 'A'
    assert num_2_str(str_2_num('IG')) == 'IG'
    assert num_2_str(str_2_num('JF')) == 'JF'


def test_basic_utils():
    assert get_letters()[0] == 'A'
    assert len(get_letters()) == 26
