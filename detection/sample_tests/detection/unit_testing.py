import unittest
import preparation_functions as pf
import error_detection_functions as edf
import error_correction_functions as ecf
import exporting_functions as ef


class ErrorTotalTests(unittest.TestCase):
    def test_filtered_total_errors_detected(self):
        """Test with profanity filter on"""
        text_list, timestamps = pf.get_file("GenerateSRT.txt")
        client = pf.initialize_api()
        sentences = pf.print_sentences(text_list)
        final_error_total = 0

        for i, token in enumerate(sentences):
            sequence_switched, end_matches, offset_list, err_message, sentence_error_total = \
                edf.detect_errors(str(sentences[i]), client, False)

            final_error_total += sentence_error_total

        self.assertEqual(final_error_total, 8)

    def test_unfiltered_total_errors_detected(self):
        """Test with profanity filter off"""
        text_list, timestamps = pf.get_file("GenerateSRT.txt")
        client = pf.initialize_api()
        sentences = pf.print_sentences(text_list)
        final_error_total = 0

        for i, token in enumerate(sentences):
            sequence_switched, end_matches, offset_list, err_message, sentence_error_total = \
                edf.detect_errors(str(sentences[i]), client, True)

            final_error_total += sentence_error_total

        self.assertEqual(final_error_total, 6)

    def test_error_type_detected(self):
        client = pf.initialize_api()
        test_str = "An eror in a short sentence."
        _, _, _, err_message, _ = \
            edf.detect_errors(test_str, client, False)

        self.assertEqual(err_message, "Spelling mistake")

    def test_multiple_error_types_detected(self):
        client = pf.initialize_api()
        test_str = "An eror in a shit short sentence."
        _, _, _, err_message, _ = \
            edf.detect_errors(test_str, client, False)

        self.assertEqual(err_message, "Spelling mistake, Profanity, ")

    def test_unfiltered_multiple_error_types_detected(self):
        client = pf.initialize_api()
        test_str = "An eror in a shit short sentence."
        _, _, _, err_message, _ = \
            edf.detect_errors(test_str, client, True)

        self.assertEqual(err_message, "Spelling mistake, ")


if __name__ == '__main__':
    unittest.main()
