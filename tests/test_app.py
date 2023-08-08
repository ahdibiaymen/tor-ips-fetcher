from src.utils import exclude_list, is_valid_ip


def test_check_bad_ip():
    ip = "ashfdsqf"
    assert is_valid_ip(ip) == False


def test_check_bad_ip2():
    ip = "10.192.2.1223"
    assert is_valid_ip(ip) == False


def test_check_valid_ip():
    ip = "10.192.2.12"
    assert is_valid_ip(ip) == True


def test_exclude_list():
    a = [1, 3, 9, 12]
    b = [2, 3, 9, 14]
    diff = exclude_list(a, b)
    assert set(diff) == {1, 12}


def test_exclude_list2():
    a = [1, 3, 9, 12]
    b = []
    diff = exclude_list(a, b)
    assert set(diff) == {1, 3, 9, 12}


def test_exclude_same_list():
    a = [1, 3, 9, 12]
    b = [1, 3, 9, 12]
    diff = exclude_list(a, b)
    assert set(diff) == set([])


def test_exclude_empty_list():
    a = []
    b = []
    diff = exclude_list(a, b)
    assert set(diff) == set([])
