"""Auto tests for Pen"""
import pytest
from pen import Pen

@pytest.fixture
def pen():
    return Pen()

# 1
def test_init_default_values(pen):
    assert pen.ink_container_value == 1000
    assert pen.size_letter == 1.0
    assert pen.color == 'blue'

# 2
@pytest.mark.parametrize("ink,size,color",[(500, 2.0, 'red')])
def test_init_custom_values(ink, size, color):
    pen = Pen(ink_container_value=ink, size_letter=size, color=color)
    assert pen.ink_container_value == ink
    assert pen.size_letter == size
    assert pen.color == color

# 3
def test_get_color_returns_default_color(pen):
    assert pen.get_color() == 'blue'

# 4
# @pytest.mark.xfail(reason='Новый цвет не записывается')
@pytest.mark.parametrize('color', ['red'])
def test_get_color_return_correct_color(color):
    pen = Pen(color=color)
    assert pen.get_color() == color

# 5
@pytest.mark.parametrize('value, expected', [(0, False), (1000, True), (-1, False), (1, True)])
def test_check_pen_state(value, expected):
    pen = Pen(ink_container_value=value)
    assert pen.check_pen_state() is expected

# 6
# @pytest.mark.xfail(reason='Метод ничего не возвращает')
def test_do_something_else_prints_color(capsys):
    result = Pen(color='green').do_something_else()
    assert capsys.readouterr().out == 'green\n'
    assert result is not None

# 7
@pytest.mark.parametrize('word', ['hello'])
def test_write_return_full_word_if_ink_is_enough(pen, word):
    assert pen.write(word) == word

# 8
# @pytest.mark.xfail(reason='Тип ink неправильный, должен быть int как указано в __init__')
@pytest.mark.parametrize('size_letter, expected_ink', [(1.0, 95), (3.0, 85), (1.5, 92.5)])
def test_write_decreases_ink_by_word_size(size_letter, expected_ink):
    test_pen = Pen(ink_container_value=100, size_letter=size_letter)
    test_pen.write('hello')
    assert test_pen.ink_container_value == expected_ink
    assert isinstance(test_pen.ink_container_value, int)

# 9
@pytest.mark.parametrize('word', ['hello'])
def test_write_return_full_word_if_ink_has_the_same_size_as_word(word):
    test_pen = Pen(ink_container_value=5)
    assert test_pen.write(word) == word
    assert test_pen.ink_container_value == 0

# 10
@pytest.mark.parametrize('word', ['hello'])
def test_write_return_cutted_word_if_ink_is_not_enough(word):
    test_pen = Pen(ink_container_value=3)
    assert test_pen.write(word) == word[:3]
    assert test_pen.ink_container_value == 0

# 11
# @pytest.mark.xfail(reason='Учитывая размер букв, слово должно быть обрезано, т.к. чернил не хватит')
@pytest.mark.parametrize('word', ['hello'])
def test_write_return_cutted_word_if_size_letter_multiple_word_length_more_than_ink(word):
    test_pen = Pen(ink_container_value=5, size_letter=2.0)
    assert test_pen.write(word) == word[:2]
    assert test_pen.ink_container_value == 0

# 12
# @pytest.mark.xfail(reason='TypeError при повторном вызове')
def test_write_should_work_after_first_call():
    test_pen = Pen(ink_container_value=15)
    assert test_pen.write('abc') == 'abc'
    assert test_pen.write('test123456789') == 'test123456789'

# 13
@pytest.mark.parametrize('word', ['hello'])
def test_write_returns_empty_string_when_ink_zero(word):
    test_pen = Pen(ink_container_value=0)
    assert test_pen.write(word) == ''