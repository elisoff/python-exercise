import random
import sqlite3

from sequence_db import SequenceDb


def generate_random_sequence():
    accepted_values = ['A', 'C', 'G', 'T']
    sequence_size = random.randrange(4, 10)

    random_sequence = random.choices(accepted_values, k=sequence_size)

    return ''.join(random_sequence)


sequence_db = SequenceDb()

try:

    random_sequence = generate_random_sequence()
    insert_row_id = sequence_db.insert(random_sequence)

    id_one_value = sequence_db.get(1)
    has_overlap = sequence_db.overlap('GAGA', 1)
    found_value = sequence_db.find('GA')
    new_id_value = sequence_db.get(insert_row_id)

    print('New row id =', insert_row_id, '| ID 1 value =',
          id_one_value, '| Is GA overlapped on ID 1 =', has_overlap, 'Result for find GAGA =', found_value, 'New row value =', new_id_value)
except Exception as e:
    print(e)

try:
    sequence_db.insert('ABCDE')
except Exception as e:
    print(e)

try:
    invalid_sequence = sequence_db.find('AAAABBB')
except Exception as e:
    print(e)
