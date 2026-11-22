"""Run after build.bat: python -m unittest discover -s tests -v"""
import unittest
import scanner

class FinalProjectTests(unittest.TestCase):
    def setUp(self):
        scanner.clear_history()

    def tearDown(self):
        scanner.clear_history()

    def test_safe_message(self):
        result = scanner.scan("SMS", "Hi, are we meeting for lunch tomorrow?", "", {})
        self.assertEqual(result["risk_score"], 0)
        self.assertEqual(result["risk_level"], "Safe")

    def test_shipping_word_does_not_match_pin(self):
        result = scanner.scan("SMS", "Your shipping update is ready for collection.", "", {})
        self.assertEqual(result["risk_score"], 0)
        self.assertEqual(result["risk_level"], "Safe")

    def test_ordinary_banking_notice_is_not_automatically_scam(self):
        result = scanner.scan("SMS", "Your bank statement is ready in the official mobile app.", "", {})
        self.assertEqual(result["risk_level"], "Safe")

    def test_scam_url(self):
        result = scanner.scan("URL", "", "https://google.com@192.168.4.20/verify", {})
        self.assertEqual(result["risk_score"], 55)
        self.assertEqual(result["risk_level"], "Suspicious")
        self.assertIn("@", result["reasons"])

    def test_history_and_stack_undo(self):
        scanner.scan("SMS", "urgent OTP", "", {})
        scanner.scan("URL", "", "https://bit.ly/login", {})
        self.assertEqual(scanner.read_history()[0]["Input type"], "URL")
        self.assertEqual(len(scanner.read_history("Shortened")), 1)
        self.assertEqual(scanner.undo_last_scan(), "2")
        self.assertEqual(len(scanner.read_history()), 1)

    def test_empty_input_is_an_error(self):
        with self.assertRaises(ValueError): scanner.scan("SMS", "", "", {})

    def test_invalid_url_is_an_error(self):
        with self.assertRaises(ValueError): scanner.scan("URL", "", "not a url", {})

    def test_qr_content_routing_rules(self):
        self.assertTrue(scanner.looks_like_url("https://example.com"))
        self.assertFalse(scanner.looks_like_url("not a url"))

    def test_missing_executable_error(self):
        old = scanner.dsa_engine_path
        scanner.dsa_engine_path = lambda: scanner.ROOT / "missing_dsa.exe"
        try:
            with self.assertRaisesRegex(RuntimeError, "missing"): scanner.run_engine(["LIST"])
        finally:
            scanner.dsa_engine_path = old

if __name__ == "__main__": unittest.main(verbosity=2)
