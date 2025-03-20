from ed318_pydantic.util import get_list_depth


def test_get_list_depth():
    assert get_list_depth(17) == 0

    assert get_list_depth([1]) == 1

    assert get_list_depth([[1]]) == 2
    assert get_list_depth([[1, 2], [3, 4]]) == 2

    assert get_list_depth([[[1, 2, 3]]]) == 3


def test_get_list_depth_corner_cases():
    assert get_list_depth("a") == 0
    assert get_list_depth("abc") == 0
    assert get_list_depth(["abc"]) == 1

    assert get_list_depth(b"a") == 0
    assert get_list_depth(b"abc") == 0
    assert get_list_depth([b"abc"]) == 1
