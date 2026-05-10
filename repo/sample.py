"""
Sample Python code with intentional bugs.
"""


def divide_numbers(a, b):
    """
    Divide two numbers.

    Bug: Division by zero not handled
    Bug: No type validation
    """
    result = a / b
    return result


def get_element(items, index):
    """
    Get element from a list using index.

    Bug: Index out of range not handled
    Bug: Doesn't handle negative index properly
    """
    return items[index]


def reverse_text(text):
    """
    Reverse a string.

    Bug: Doesn't handle None input
    Bug: No type validation
    """
    reversed_text = text[::-1]
    return reversed_text


def calculate_square_root(number):
    """
    Calculate square root of a number.

    Bug: Negative numbers not handled
    Bug: No type validation
    """
    return number ** 0.5


def count_words(sentence):
    """
    Count number of words in a sentence.

    Bug: Doesn't handle empty string properly
    Bug: Doesn't handle None input
    
    """
    words = sentence.split(" ")
    return len(words)