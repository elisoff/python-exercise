import sqlite3


class SequenceDb:
    """Manipulate sequence data from the db"""

    def __init__(self, conn):
        self.conn = conn
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()

        try:
            cursor.execute(
                '''create table if not exists sequences
                    (id integer primary key, dna_sequence varchar unique)'''
            )
        except sqlite3.Error:
            raise ConnectionError('Error creating table')

    @staticmethod
    def is_input_valid(dna_sequence: str) -> bool:
        """
            Check if a DNA Sequence input is valid:
            It should only contain ‘A', ‘C’, ‘G’ and 'T’
        """

        if not dna_sequence:
            return False

        if all(sequence_value in 'ACGT' for sequence_value in dna_sequence):
            return True

        return False

    def insert(self, dna_sequence: str) -> int:
        """
        Inserts a new DNA sequence into the sequences table.
        DNA sequences are unique and should only contain the
        valid caracters.
        """

        if not self.is_input_valid(dna_sequence):
            raise ValueError('Invalid DNA Sequence input')

        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(
                    "insert into sequences(dna_sequence) values (?)",
                    (dna_sequence,)
                )
            last_row_id = cursor.lastrowid
            cursor.close()

            return last_row_id
        except sqlite3.IntegrityError:
            raise ValueError('DNA Sequence already exists')

    def get(self, dna_sequence_id: int) -> str:
        """
        Retrieves a DNA sequence with the received id.
        """

        if not isinstance(dna_sequence_id, int):
            raise TypeError('dna_sequence_id should be an integer')

        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(
                    "select id, dna_sequence from sequences where id = ?",
                    (dna_sequence_id,)
                )
            results = [row['dna_sequence'] for row in cursor]

            cursor.close()

            if len(results) == 1:
                return results[0]

            return None
        except sqlite3.Error:
            raise ConnectionError(
                'Something went wrong retrieving the register'
            )

    def find(self, sample: str) -> list:
        """
        Searches for a DNA sequence based on the sample.
        """

        if not self.is_input_valid(sample):
            raise ValueError('Invalid sample')

        try:
            formatted_sample = '%{sample}%'.format(sample=sample)

            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(
                    '''select id, dna_sequence from sequences
                        where dna_sequence like ?''', (formatted_sample,)
                )
            results = [row['id'] for row in cursor]

            cursor.close()

            if len(results) > 0:
                return results

            return []
        except sqlite3.Error as e:
            raise ConnectionError(e)
