import pytest

class Pen(object):
    def __init__(self, **kwargs):
        # the amount of ink
        self.ink_container_value = int(kwargs.get('ink_container_value', 1000))
        # size of the letter (font)
        self.size_letter = float(kwargs.get('size_letter', 1.0))
        # ink color
        self.color = str(kwargs.get('color', 'blue'))

    def write(self, word):
        if not self.check_pen_state():
            return ''
        size_of_word = len(word) * self.size_letter
        if size_of_word <= self.ink_container_value:
            self.ink_container_value -= size_of_word
            return word
        part_of_word = word[0: self.ink_container_value]
        self.ink_container_value = 0
        return part_of_word

    def get_color(self):
        return 'blue'

    def check_pen_state(self):
        return self.ink_container_value > 0

    def do_something_else(self):
        print(self.color)

# Tests

# 1
def test_init_default_values():
    pen = Pen()

    assert pen.ink_container_value == 1000
    assert pen.size_letter == 1.0
    assert pen.color == 'blue'

#2
@pytest.mark.parametrize("ink,size,color",[(500, 2.0, 'red')])
def test_init_custom_values(ink, size, color):
    pen = Pen(ink_container_value=ink, size_letter=size, color=color)
    assert pen.ink_container_value == ink
    assert pen.size_letter == size
    assert pen.color == color

# 3
@pytest.mark.xfail(reason='Метод всегда возвращает blue')
@pytest.mark.parametrize('color', ['red'])
def test_get_color_return_correct_color(color):
    pen = Pen(color=color)
    assert pen.get_color() == color

# 4
@pytest.mark.parametrize('value, expected', [(0, False), (1000, True), (-1, False), (1, True)])
def test_check_pen_state(value, expected):
    pen = Pen(ink_container_value=value)
    assert pen.check_pen_state() is expected

@pytest.mark.parametrize('word', ['hello'])
def test_write_return_empty_string_when_ink_zero(word):
    pen = Pen(ink_container_value=0)
    assert pen.write(word) == ''

@pytest.mark.parametrize('word', ['hello'])
def test_write_return_full_word(word):
    pen = Pen(ink_container_value=100)
    assert pen.write(word) == word

