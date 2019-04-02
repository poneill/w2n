from __future__ import print_function

from decimal import Decimal

american_number_system = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90,
    'hundred': 100,
    'thousand': 10**3,
    'million': 10**6,
    'billion': 10**9,
    'trillion': 10**12,
    'point': '.'
}

decimal_words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

three_digit_postfixes = {
    'trillion': 10**12,
    'billion': 10**9,
    'million': 10**6,
    'thousand': 10**3
}

"""
#TODO
indian_number_system = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90,
    'hundred': 100,
    'thousand': 1000,
    'lac': 100000,
    'lakh': 100000,
    'crore': 10000000
}
"""

"""
function to form numeric multipliers for million, billion, thousand etc.

input: list of strings
return value: integer
"""



def number_formation(number_words):
    numbers = []
    for number_word in number_words:
        numbers.append(american_number_system[number_word])
    if len(numbers) == 4:
        return (numbers[0] * numbers[1]) + numbers[2] + numbers[3]
    elif len(numbers) == 3:
        return numbers[0] * numbers[1] + numbers[2]
    elif len(numbers) == 2:
        if 100 in numbers:
            return numbers[0] * numbers[1]
        else:
            return numbers[0] + numbers[1]
    else:
        return numbers[0]


"""
function to convert post decimal digit words to numerial digits
input: list of strings
output: double
"""


def get_decimal_sum(decimal_digit_words):
    decimal_number_str = []
    for dec_word in decimal_digit_words:
        if(dec_word not in decimal_words):
            return 0
        else:
            decimal_number_str.append(american_number_system[dec_word])
    final_decimal_string = '0.' + ''.join(map(str,decimal_number_str))
    return Decimal(final_decimal_string)


"""
function to return integer for an input `number_sentence` string
input: string
output: int or double or None
"""


def word_to_num(number_sentence):
    if type(number_sentence) is not str:
        raise ValueError("Type of input is not string! Please enter a valid number word (eg. \'two million twenty three thousand and forty nine\')")

    number_sentence = number_sentence.replace('-', ' ')
    number_sentence = number_sentence.lower()  # converting input to lowercase

    if(number_sentence.isdigit()):  # return the number if user enters a number string
        return Decimal(number_sentence)

    split_words = number_sentence.strip().split()  # strip extra spaces and split sentence into words

    clean_numbers = []
    clean_decimal_numbers = []

    # removing and, & etc.
    for word in split_words:
        if word in american_number_system:
            clean_numbers.append(word)


    # Error message if the user enters invalid input!
    if len(clean_numbers) == 0:
        raise ValueError("No valid number words found! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")


    # separate decimal part of number (if exists)
    if clean_numbers.count('point') == 1:
        clean_decimal_numbers = clean_numbers[clean_numbers.index('point')+1:]
        clean_numbers = clean_numbers[:clean_numbers.index('point')]

    # billion_index = clean_numbers.index('billion') if 'billion' in clean_numbers else -1
    # million_index = clean_numbers.index('million') if 'million' in clean_numbers else -1
    # thousand_index = clean_numbers.index('thousand') if 'thousand' in clean_numbers else -1
    _validate_clean_numbers(clean_numbers)

    # if (thousand_index > -1 and (thousand_index < million_index or thousand_index < billion_index)) or (million_index>-1 and million_index < billion_index):
    #     raise ValueError("Malformed number! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")

    #  groups represents clean_numbers, split into three digit groupings.
    # e.g. ['two', 'million', 'twenty', 'three', 'thousand', 'forty', 'nine'] =>
    # [['two', 'million'], ['twenty', 'three', 'thousand'], ['forty', 'nine']]
    groups = []
    group = []
    for word in clean_numbers:
        group.append(word)
        if word in three_digit_postfixes:
            groups.append(group[:])
            group = []
    if group:
        groups.append(group)

    total_sum = Decimal(0)  # storing the number to be returned
    for group in groups:
        if group[-1] in three_digit_postfixes:
            three_digit_number_word, postfix = group[:-1], group[-1]
        else:  # the last three digits...
            three_digit_number_word, postfix = group, 'unit'
        if three_digit_number_word:
            three_digit_number = number_formation(three_digit_number_word)
        # else if there is no three_digit_number_word, a bare postfix like
        # 'thousand' should be interpreted as 1,000
        else:
            three_digit_number = 1
        postfix_value = three_digit_postfixes.get(postfix, 1)
        total_sum += three_digit_number * postfix_value

    # adding decimal part to total_sum (if exists)
    if len(clean_decimal_numbers) > 0:
        #  we multiply and divide by roundoff constant in order to add
        #  total_sum and decimal_sum far away from 1.0, in order to
        #  avoid roundoff error
        decimal_sum = get_decimal_sum(clean_decimal_numbers)
        total_sum += decimal_sum

    total_sum = _from_decimal(total_sum)
    return total_sum


def _validate_clean_numbers(clean_numbers):
    """Make sure that 'millions', 'billions' &c. don't occur out of order."""

        # Error if user enters million,billion, thousand or decimal point twice
    unique_words = list(three_digit_postfixes.keys()) + ['point']
    if any(clean_numbers.count(w) > 1 for w in unique_words):
        raise ValueError("Redundant number word! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")

    three_digit_indices = {
        w: clean_numbers.index(w)
        for w in three_digit_postfixes
        if w in clean_numbers
    }
    for w1, idx1 in three_digit_indices.items():
        val1 = three_digit_postfixes[w1]
        for w2, idx2 in three_digit_indices.items():
            val2 = three_digit_postfixes[w2]
            one_before_two = (val1 <= val2)
            one_greater_than_two = (idx1 >= idx2)
            if not one_before_two == one_greater_than_two:
                raise ValueError("Malformed number! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")


def _from_decimal(d):
    """Convert decimal back to int or float."""
    if (d - d.to_integral()).is_zero():
        return int(d)
    else:
        return float(d)
