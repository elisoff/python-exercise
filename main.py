#!/usr/bin/python3
import random
from sequence_db import SequenceDb
import sqlite3


def generate_random_sequence():
    accepted_values = ['A', 'C', 'G', 'T']
    sequence_size = random.randrange(4, 10)

    random_sequence = random.choices(accepted_values, k=sequence_size)

    return ''.join(random_sequence)


def execute_sequence_db():
    sequence_db = SequenceDb(sqlite3.connect('sequence.db'))

    try:

        random_sequence = generate_random_sequence()
        insert_row_id = sequence_db.insert(random_sequence)

        id_one_value = sequence_db.get(1)
        found_value = sequence_db.find('GA')
        new_id_value = sequence_db.get(insert_row_id)
        has_overlap = sequence_db.overlap('GAGA', insert_row_id)

        print(
            '''New row id = {0} | ID 1 value = {1} | Result for find GAGA =
            {2} | New row value = {3} - has overlap with GAGA = {4}'''.format(
                insert_row_id, id_one_value, found_value,
                new_id_value, has_overlap
            )
        )
    except Exception as e:
        print(e)

    try:
        sequence_db.insert('ABCDE')
    except Exception as e:
        print(e)

    try:
        sequence_db.find('AAAABBB')
    except Exception as e:
        print(e)


execute_sequence_db()
