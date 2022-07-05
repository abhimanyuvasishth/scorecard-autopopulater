from scorecard_autopopulater.dismissal import Dismissal, DismissalType


def test_dismissal():
    test_cases = [
        ('c †Dickwella b Chameera', 'Dickwella', 'Chameera', DismissalType.CAUGHT),
        ('run out (sub (Shankar)/Dube)', 'Shankar', None, DismissalType.RUN_OUT),
        ('st Rishabh Pant † b Avesh', 'Rishabh Pant', 'Avesh', DismissalType.STUMPED),
        ('run out (Shankar)', 'Shankar', None, DismissalType.RUN_OUT),
        ('b Chameera', None, None, DismissalType.OTHER),
        ('c de Silva b Lakmal', 'de Silva', 'Lakmal', DismissalType.CAUGHT),
        ('c sub (du Plessis) b Harshal', 'du Plessis', 'Harshal', DismissalType.CAUGHT),
        ('st sub (†de Kock) b Chameera', 'de Kock', 'Chameera', DismissalType.STUMPED),
        ('c Virat Kohli (c) b Harshal', 'Virat Kohli', 'Harshal', DismissalType.CAUGHT),
        ('c & b Harshal', 'Harshal', 'Harshal', DismissalType.CAUGHT),
    ]

    for text, fielder, bowler, dismissal_type in test_cases:
        dismissal = Dismissal(text)
        assert dismissal.dismissal == text
        assert dismissal.fielder == fielder
        assert dismissal.bowler == bowler
        assert dismissal.dismissal_type == dismissal_type
