from match import Match
from utils import letter_to_number, number_to_letter, safe_int, safe_float, \
    get_letters, extract_fielder_name, extract_name

def test_column_number_conversion():
    assert number_to_letter(letter_to_number('A')) == 'A'
    assert number_to_letter(letter_to_number('IG')) == 'IG'
    assert number_to_letter(letter_to_number('JF')) == 'JF'

def test_basic_utils():
    assert safe_int('2') == 2
    assert safe_int('abc') == 0
    assert safe_float('2') == 2.0
    assert safe_float('abc') == 0.0
    assert get_letters()[0] == 'A'
    assert len(get_letters()) == 26

def test_extract_players():
    assert extract_name('Virat Kohli (c)') == 'Virat Kohli'
    assert extract_name('Rishabh Pant †') == 'Rishabh Pant'
    assert extract_fielder_name('(Shankar)') == 'Shankar'
    assert extract_fielder_name('(du Plessis)') == 'du Plessis'

def test_extract_dismissal():
    assert Match.extract_caught_or_stumped('c †Dickwella b Chameera') == 'Dickwella'
    assert Match.extract_caught_or_stumped('c de Silva b Lakmal') == 'de Silva'
    assert Match.extract_run_out('run out (Shankar)') == 'Shankar'

def test_extract_sub():
    assert Match.extract_run_out('run out (sub (Shankar)/Dube)') == 'Shankar'
    assert extract_fielder_name('sub (du Plessis)') == 'du Plessis'
