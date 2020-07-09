from collections import Counter, defaultdict
from math import log, pi
from pprint import pprint
from decimal import Decimal
from fractions import Fraction

import pandas as pd
import string

STOP_WORDS = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

TABLE = str.maketrans("", "", string.punctuation)


def parse(txt):
    words = []
    for word in txt.split(' '):
        word = word.translate(TABLE)

        if word.lower() in STOP_WORDS or len(word) < 2 or word.isnumeric():
            continue
        words.append(word.lower())

    return list(set(words))


def calc(probability, has_x_int):
    return has_x_int * log(probability / (1 - probability)) + log(1 - probability)


def smooth(rate):
    _fraction = Fraction(rate).limit_denominator(1000)
    return (_fraction.numerator + 10) / (_fraction.denominator + 10)


def main():
    df = pd.read_json('articles.json').sample(frac=1)
    section_names = list(df.section_name.unique())
    rows = df.to_dict('records')
    train_rows = rows[:1200]
    test_rows = rows[:300]

    vocabs = defaultdict(dict)
    for section_name in section_names:
        words = []
        _rows = [r for r in train_rows if section_name == r['section_name']]
        top_section_words = {}
        for row in _rows:
            words += parse(row['lead_paragraph'])
        c = Counter(words)
        for k, v in c.most_common(100):
            top_section_words[k] = smooth(v / len(_rows))

        vocabs[section_name] = top_section_words

    match = 0
    for row in test_rows:
        max_section = None
        max_score = 0
        for section_name, words in vocabs.items():
            print('=====')

            score = 0
            for word, probability in words.items():
                _words = parse(row['lead_paragraph'])
                has_word_int = 1 if word in _words else 0
                score += calc(probability, has_word_int)

            print(section_name, score)
            if not max_score or score > max_score:
                max_section = section_name
                max_score = score

        if max_section == row['section_name']:
            match += 1
        else:
            print('incorrect', row['section_name'], max_section)

    print(match / len(test_rows))




if __name__ == '__main__':
    main()
