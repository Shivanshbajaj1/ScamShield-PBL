"""Combined input tests. Run after building both scamshield.exe and scamshield_dsa.exe."""
import unittest
import scanner


class CombinedScanningTests(unittest.TestCase):
    def setUp(self):
        scanner.clear_history()

    def tearDown(self):
        scanner.clear_history()

    def test_sms_and_url_are_scored_together(self):
        result = scanner.scan_combined(
            {"SMS": "URGENT! Your account is blocked. Send your OTP immediately."},
            ["https://bit.ly/login"],
            {},
        )
        self.assertEqual(result["risk_score"], 75)
        self.assertEqual(result["risk_level"], "Scam")
        self.assertEqual(result["sources"], ["SMS", "URL"])

    def test_qr_and_screenshot_text_can_be_combined(self):
        result = scanner.scan_combined(
            {
                "QR code": "Claim your prize now.",
                "Screenshot": "Your account is suspended. Pay a fee immediately.",
            },
            [],
            {},
            extra_sources=["QR code", "Screenshot"],
        )
        self.assertEqual(result["risk_score"], 50)
        self.assertEqual(result["sources"], ["QR code", "Screenshot"])
        self.assertEqual(result["input_type"], "QR+OCR")

    def test_same_finding_is_not_counted_twice_across_sources(self):
        result = scanner.scan_combined(
            {"SMS": "Send your OTP now.", "Screenshot": "Send your OTP now."},
            [],
            {},
        )
        self.assertEqual(result["risk_score"], 20)
        self.assertEqual(result["input_type"], "SMS+OCR")

    def test_multiple_urls_are_checked_in_one_scan(self):
        result = scanner.scan_combined(
            {"SMS": "Please review these links."},
            ["https://bit.ly/login", "https://secure.example.com/verify"],
            {},
        )
        self.assertEqual(len(result["urls_checked"]), 2)
        self.assertEqual(result["risk_score"], 30)

    def test_c_evidence_linked_list_deduplicates_findings_from_multiple_urls(self):
        result = scanner.scan_combined(
            {},
            ["https://bit.ly/login", "https://tinyurl.com/verify"],
            {},
        )
        self.assertEqual(result["risk_score"], 30)
        self.assertEqual(result["reasons"].count("Uses a shortened URL"), 1)
        self.assertEqual(result["reasons"].count("URL contains account or verification wording"), 1)

    def test_url_in_sms_is_also_sent_to_url_scanner(self):
        result = scanner.scan_combined(
            {"SMS": "Check this page https://bit.ly/login"},
            [],
            {},
        )
        self.assertEqual(result["risk_score"], 30)
        self.assertIn("URL", result["sources"])

    def test_manual_url_domain_without_scheme_is_accepted(self):
        self.assertTrue(scanner.looks_like_url("google.com"))
        result = scanner.scan_combined({}, ["google.com"], {})
        self.assertEqual(result["urls_checked"], ["https://google.com"])

    def test_invalid_url_is_reported_but_valid_sms_is_still_scanned(self):
        result = scanner.scan_combined({"SMS": "Send your OTP."}, ["not a url"], {})
        self.assertEqual(result["risk_score"], 20)
        self.assertEqual(result["invalid_urls_skipped"], ["not a url"])

    def test_all_four_sources_create_one_combined_result(self):
        result = scanner.scan_combined(
            {
                "SMS": "Urgent action needed.",
                "QR code": "You have won a prize.",
                "Screenshot": "Your account is suspended. Pay a fee.",
            },
            ["https://bit.ly/login"],
            {},
            extra_sources=["QR code", "Screenshot"],
        )
        self.assertEqual(result["input_type"], "SMS+URL+QR+OCR")
        self.assertEqual(result["risk_score"], 80)
        self.assertEqual(result["risk_level"], "Scam")
        self.assertEqual(len(scanner.read_history()), 1)

    def test_every_two_source_pair_can_be_scanned_together(self):
        pairs = [
            ({"SMS": "Urgent notice."}, ["https://bit.ly/login"], [], "SMS+URL"),
            ({"SMS": "Urgent notice.", "QR code": "You have won a prize."}, [], ["QR code"], "SMS+QR"),
            ({"SMS": "Urgent notice.", "Screenshot": "Your account is suspended."}, [], ["Screenshot"], "SMS+OCR"),
            ({"QR code": "You have won a prize."}, ["https://bit.ly/login"], ["QR code"], "URL+QR"),
            ({"Screenshot": "Your account is suspended."}, ["https://bit.ly/login"], ["Screenshot"], "URL+OCR"),
            ({"QR code": "You have won a prize.", "Screenshot": "Your account is suspended."}, [], ["QR code", "Screenshot"], "QR+OCR"),
        ]
        for text_sources, urls, extra_sources, expected_type in pairs:
            scanner.clear_history()
            result = scanner.scan_combined(text_sources, urls, {}, extra_sources)
            self.assertGreater(result["risk_score"], 0)
            self.assertEqual(result["input_type"], expected_type)
            self.assertEqual(len(scanner.read_history()), 1)

    def test_every_three_source_combination_can_be_scanned_together(self):
        triples = [
            ({"SMS": "Urgent notice.", "QR code": "You have won a prize."}, ["https://bit.ly/login"], ["QR code"], "SMS+URL+QR"),
            ({"SMS": "Urgent notice.", "Screenshot": "Your account is suspended."}, ["https://bit.ly/login"], ["Screenshot"], "SMS+URL+OCR"),
            ({"SMS": "Urgent notice.", "QR code": "You have won a prize.", "Screenshot": "Your account is suspended."}, [], ["QR code", "Screenshot"], "SMS+QR+OCR"),
            ({"QR code": "You have won a prize.", "Screenshot": "Your account is suspended."}, ["https://bit.ly/login"], ["QR code", "Screenshot"], "URL+QR+OCR"),
        ]
        for text_sources, urls, extra_sources, expected_type in triples:
            scanner.clear_history()
            result = scanner.scan_combined(text_sources, urls, {}, extra_sources)
            self.assertGreater(result["risk_score"], 0)
            self.assertEqual(result["input_type"], expected_type)
            self.assertEqual(len(scanner.read_history()), 1)

    def test_combined_history_is_one_record(self):
        scanner.scan_combined(
            {"SMS": "Urgent OTP request."},
            ["https://bit.ly/login"],
            {},
        )
        history = scanner.read_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["Input type"], "SMS+URL")


if __name__ == "__main__":
    unittest.main(verbosity=2)
