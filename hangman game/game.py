from .exceptions import *
import random

# Complete with your own, just for fun :)
LIST_OF_WORDS = ['PYTHON', 'JAVA', 'SQL']


def _get_random_word(list_of_words):
    if not list_of_words or not all(isinstance(word, str) for word in list_of_words):
        raise InvalidListOfWordsException("The word list is invalid.")
    return random.choice(list_of_words).upper()


def _mask_word(word):
    if not isinstance(word, str) or not word.isalpha():
        raise InvalidWordException("The word is invalid.")
    return '*' * len(word)


def _uncover_word(answer_word, masked_word, character):
    if not isinstance(answer_word, str) or not isinstance(masked_word, str) or not isinstance(character, str):
        raise InvalidGuessedLetterException("Invalid input.")
    if len(character) != 1 or not character.isalpha():
        raise InvalidGuessedLetterException("Guessed letter must be a single alphabetic character.")
    character = character.upper()

    if character in answer_word:
        return ''.join(character if answer_word[i] == character else masked_word[i] for i in range(len(answer_word)))
    return masked_word


def guess_letter(game, letter):
    if not isinstance(game, dict) or 'answer_word' not in game or 'masked_word' not in game:
        raise ValueError("Invalid game state.")
    if letter in game['previous_guesses']:
        return  # The letter has already been guessed

    game['previous_guesses'].append(letter)
    new_masked_word = _uncover_word(game['answer_word'], game['masked_word'], letter)

    if new_masked_word == game['masked_word']:
        game['remaining_misses'] -= 1
        if game['remaining_misses'] <= 0:
            raise GameLostException("No more attempts left.")
    else:
        game['masked_word'] = new_masked_word

    if '*' not in game['masked_word']:
        raise GameWonException("Congratulations! You have won the game.")


def start_new_game(list_of_words=None, number_of_guesses=5):
    if list_of_words is None:
        list_of_words = LIST_OF_WORDS

    word_to_guess = _get_random_word(list_of_words)
    masked_word = _mask_word(word_to_guess)
    game = {
        'answer_word': word_to_guess,
        'masked_word': masked_word,
        'previous_guesses': [],
        'remaining_misses': number_of_guesses,
    }

    return game