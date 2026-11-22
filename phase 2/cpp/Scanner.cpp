#include "Scanner.h"
#include <algorithm>
#include <cctype>

using namespace std;

static string lower(string text) {
    for (char &letter : text) letter = (char)tolower((unsigned char)letter);
    return text;
}


static bool has_word(const string &text, const string &word) {
    size_t place = text.find(word);
    while (place != string::npos) {
        bool left_ok = place == 0 || !isalnum((unsigned char)text[place - 1]);
        size_t end = place + word.length();
        bool right_ok = end == text.length() || !isalnum((unsigned char)text[end]);
        if (left_ok && right_ok) return true;
        place = text.find(word, place + 1);
    }
    return false;
}

Scanner::Scanner(const string &name) { scanner_name = name; }
string Scanner::name() const { return scanner_name; }
MessageScanner::MessageScanner() : Scanner("Message scanner") {}
URLScanner::URLScanner() : Scanner("URL scanner") {}

void add_finding(vector<Finding> &findings, const string &name, const string &reason, int points) {
    /* The C evidence linked list removes repeated finding names centrally. */
    findings.push_back({name, reason, points});
}

void MessageScanner::scan(const string &input, vector<Finding> &findings) {
    string text = lower(input);
    if (has_word(text, "otp") || has_word(text, "pin") || has_word(text, "cvv") || has_word(text, "password"))
        add_finding(findings, "credentials", "Requests OTP, PIN, CVV or password", 20);
    if (has_word(text, "urgent") || has_word(text, "immediately"))
        add_finding(findings, "urgency", "Uses urgent language", 10);
    if (has_word(text, "blocked") || has_word(text, "suspended"))
        add_finding(findings, "threat", "Threatens account blocking or suspension", 15);
    if (has_word(text, "winner") || has_word(text, "prize") || has_word(text, "reward") || has_word(text, "refund"))
        add_finding(findings, "lure", "Uses prize, reward or refund lure", 15);
    if (has_word(text, "pay") || has_word(text, "payment") || has_word(text, "fee"))
        add_finding(findings, "payment", "Requests payment or a fee", 10);
}

static string host_from_url(const string &url) {
    size_t start = url.find("://");
    start = start == string::npos ? 0 : start + 3;
    size_t end = url.find_first_of("/?#", start);
    string host = url.substr(start, end == string::npos ? string::npos : end - start);
    size_t at = host.rfind('@'); if (at != string::npos) host = host.substr(at + 1);
    size_t colon = host.find(':'); if (colon != string::npos) host = host.substr(0, colon);
    return host;
}

static bool is_ipv4(const string &host) {
    int groups = 0; size_t start = 0;
    while (start < host.length()) {
        size_t end = host.find('.', start); string part = host.substr(start, end == string::npos ? string::npos : end - start);
        if (part.empty() || part.length() > 3) return false;
        int value = 0; for (char letter : part) { if (!isdigit((unsigned char)letter)) return false; value = value * 10 + (letter - '0'); }
        if (value > 255) return false;
        groups++; if (end == string::npos) break; start = end + 1;
    }
    return groups == 4;
}

void URLScanner::scan(const string &input, vector<Finding> &findings) {
    string url = lower(input);
    string host = host_from_url(url);
    if (url.find('@') != string::npos) add_finding(findings, "at_symbol", "URL contains @ which can hide the destination", 20);
    if (url.find("xn--") != string::npos) add_finding(findings, "punycode", "URL contains punycode lookalike text", 15);
    if (host == "bit.ly" || host == "tinyurl.com" || host == "t.co")
        add_finding(findings, "shortener", "Uses a shortened URL", 15);
    if (url.find("login") != string::npos || url.find("verify") != string::npos || url.find("account") != string::npos || url.find("kyc") != string::npos)
        add_finding(findings, "phishing_word", "URL contains account or verification wording", 15);
    if (url.length() > 100) add_finding(findings, "long_url", "URL is unusually long", 10);
    int dots = 0; for (char letter : host) if (letter == '.') dots++;
    if (!is_ipv4(host) && dots >= 3) add_finding(findings, "subdomains", "URL has many dot-separated parts", 10);
    if (is_ipv4(host)) add_finding(findings, "ip_host", "URL uses a numeric IP address", 20);
}
