import sqlite3


class SequenceDb:

    conn = None

    def __init__(self):
        self.conn = sqlite3.connect('sequence.db')
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()

        try:
            cursor.execute(
                "create table if not exists sequences (id integer primary key, dna_sequence varchar unique)")
        except sqlite3.Error:
            raise Exception('Error creating table')

    @staticmethod
    def is_input_valid(dna_sequence):
        if not dna_sequence:
            return False

       # Input should only contain ‘A', ‘C’, ‘G’ and 'T’.
        accepted_values = ['A', 'C', 'G', 'T']
        input_values = list(dna_sequence)

        invalid_values = [
            input_value for input_value in input_values if input_value not in accepted_values]

        if len(invalid_values) > 0:
            return False

        return True

    def insert(self, dna_sequence):
        if not self.is_input_valid(dna_sequence):
            raise Exception('Invalid DNA Sequence input')

        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(
                    "insert into sequences(dna_sequence) values (?)", (dna_sequence,))
            last_row_id = cursor.lastrowid
            cursor.close()

            return last_row_id
        except sqlite3.IntegrityError:
            raise Exception('DNA Sequence already exists')

    def get(self, dna_sequence_id):
        try:
            int(dna_sequence_id)
        except ValueError:
            raise Exception('dna_sequence_id should be an integer')

        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(
                    "select id, dna_sequence from sequences where id = ?", (dna_sequence_id,))
            results = [row['dna_sequence'] for row in cursor]

            cursor.close()

            if len(results) == 1:
                return results[0]

            return None
        except sqlite3.Error:
            raise Exception('Something went wrong retrieving the register')

    def find(self, sample):
        if not self.is_input_valid(sample):
            raise Exception('Invalid sample')

        try:
            formatted_sample = '%{sample}%'.format(sample=sample)

            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(
                    "select id, dna_sequence from sequences where dna_sequence like ?", (formatted_sample,))
            results = [row['id'] for row in cursor]

            cursor.close()

            if len(results) > 0:
                return results

            return []
        except sqlite3.Error as e:
            raise Exception(e)

    def overlap(self, sample, dna_sequence_id):
        if not self.is_input_valid(sample):
            raise Exception('Invalid sample')

        try:
            formatted_sample = '%{sample}%'.format(sample=sample)

            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(
                    "select dna_sequence from sequences where id = ? and dna_sequence like ?", (dna_sequence_id, formatted_sample,))
            results = [row for row in cursor]

            cursor.close()

            if len(results) > 0:
                return True

            return False
        except sqlite3.Error as e:
            raise Exception(e)
