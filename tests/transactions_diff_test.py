import unittest
from transactions_diff import clean_commas_from_comments


class TransactionsDiffTest(unittest.TestCase):

    def test_clean_commas_from_comments(self):
        actual_input = '",p","h,","g,k",1,"2,C",D'
        expected_output = '";p","h;","g;k",1,"2;C",D'
        self.assertEqual(expected_output, clean_commas_from_comments(actual_input))


if __name__ == '__main__':
    unittest.main()
