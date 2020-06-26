import unittest
import sqlite3
from sequence_db import SequenceDb


class TestSequenceDb(unittest.TestCase):
    def setUp(self):
        self.sequence_db = SequenceDb(sqlite3.connect(':memory:'))

        return super().setUp()

    def test_insert(self):
        self.assertEqual(self.sequence_db.insert('ACCCAGA'), 1)

        with self.assertRaises(ValueError) as duplicated_sequence_exception:
            self.sequence_db.insert('ACCCAGA')

        self.assertEqual(
            duplicated_sequence_exception.exception.args[0],
            'DNA Sequence already exists'
        )

        with self.assertRaises(ValueError) as invalid_input_exception:
            self.sequence_db.insert('XXAAXX')

        self.assertEqual(
            invalid_input_exception.exception.args[0],
            'Invalid DNA Sequence input'
        )

    def test_get(self):
        self.assertIsNone(self.sequence_db.get(1))

        sequence = 'ACCCAGA'
        self.sequence_db.insert(sequence)
        self.assertEqual(self.sequence_db.get(1), sequence)

    def test_find(self):
        sequence = 'ACCCAGA'

        self.assertEqual(self.sequence_db.find(sequence), [])

        self.sequence_db.insert(sequence)
        self.assertEqual(self.sequence_db.find(sequence), [1])

    def test_overlap(self):
        self.sequence_db.insert('ACCCAGA')

        self.assertEqual(self.sequence_db.overlap('GAGA', 1), True)
        self.assertEqual(self.sequence_db.overlap('ACAC', 1), True)
        self.assertEqual(self.sequence_db.overlap('TCTC', 1), False)

        with self.assertRaises(ValueError) as invalid_id_exception:
            self.sequence_db.overlap('TCTC', 2)

        self.assertEqual(
            invalid_id_exception.exception.args[0],
            'No DNA sequence found with that id'
        )
