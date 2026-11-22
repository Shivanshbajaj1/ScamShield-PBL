"""Run after build.bat:  python -m unittest discover -s tests -v"""
import unittest

import scanner


class ScannerTests(unittest.TestCase):
    def test_safe_sms(self):
        result = scanner.scan("Hi, are we meeting for lunch tomorrow?", "", {})
        self.assertEqual(result["risk_score"], 0)
        self.assertEqual(result["risk_level"], "Safe")

    def test_shipping_does_not_match_pin(self):
        result = scanner.scan("Your shipping update is ready for collection.", "", {})
        self.assertEqual(result["risk_score"], 0)

    def test_scam_sms(self):
        result = scanner.scan("URGENT! Your account is blocked. Send your OTP immediately.", "", {})
        self.assertEqual(result["risk_score"], 45)
        self.assertEqual(result["risk_level"], "Suspicious")

    def test_suspicious_url(self):
        result = scanner.scan("", "https://google.com@192.168.4.20/verify", {})
        self.assertEqual(result["risk_score"], 55)
        self.assertIn("@", result["reasons"])

    def test_sms_and_url_together(self):
        result = scanner.scan("URGENT! Your account is blocked. Send your OTP immediately.",
                              "https://bit.ly/login", {})
        self.assertEqual(result["risk_score"], 75)
        self.assertEqual(result["risk_level"], "Scam")
        self.assertEqual(result["sources"], ["SMS", "URL"])

    def test_linked_list_removes_repeated_findings(self):
        # Both URLs are shorteners with verification words -> each finding counted once.
        result = scanner.scan("", "https://bit.ly/login\nhttps://tinyurl.com/verify", {})
        self.assertEqual(result["risk_score"], 30)
        self.assertEqual(len(result["findings"]), 2)

    def test_domain_without_https_is_accepted(self):
        result = scanner.scan("", "google.com", {})
        self.assertEqual(result["urls_checked"], ["https://google.com"])

    def test_invalid_url_is_skipped(self):
        result = scanner.scan("Send your OTP.", "not a url", {})
        self.assertEqual(result["risk_score"], 20)
        self.assertEqual(result["invalid_urls"], ["not a url"])

    def test_empty_input_is_an_error(self):
        with self.assertRaises(ValueError):
            scanner.scan("", "", {})

    def test_missing_program_error(self):
        with self.assertRaisesRegex(RuntimeError, "missing"):
            scanner.run_program(scanner.ROOT / "missing.exe", ["SCAN"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
