#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include "Scanner.h"
#include "RiskCalculator.h"

using namespace std;

/* Input for SCAN:
   SCAN
   <sms text, can be empty>
   <number of urls>
   <url 1>
   <url 2> ...                                   */
static void scan_inputs() {
    string text, count_text, url;
    vector<Finding> findings;
    MessageScanner message_scanner;
    URLScanner url_scanner;
    Scanner *scanner;

    getline(cin, text);
    getline(cin, count_text);
    int count = atoi(count_text.c_str());

    if (!text.empty()) {
        scanner = &message_scanner;          /* base pointer -> MessageScanner */
        scanner->scan(text, findings);
    }

    scanner = &url_scanner;                  /* base pointer -> URLScanner */
    for (int i = 0; i < count; i++) {
        getline(cin, url);
        if (!url.empty()) scanner->scan(url, findings);
    }

    for (int i = 0; i < (int)findings.size(); i++) {
        cout << "FINDING=" << findings[i].name << "|" << findings[i].reason << "|" << findings[i].points << "\n";
    }
}

/* Input for CALCULATE:
   CALCULATE
   <count>
   then name, reason, points (3 lines) for each finding */
static void calculate_score() {
    string count_text, name, reason, points_text;
    vector<Finding> findings;

    getline(cin, count_text);
    int count = atoi(count_text.c_str());
    for (int i = 0; i < count; i++) {
        getline(cin, name);
        getline(cin, reason);
        getline(cin, points_text);
        findings.push_back({name, reason, atoi(points_text.c_str())});
    }

    RiskCalculator calculator;
    int score = calculator.calculate(findings);
    cout << "SCORE=" << score << "\n";
    cout << "LABEL=" << calculator.label(score) << "\n";
    cout << "REASONS=" << calculator.reasons(findings) << "\n";
}

int main() {
    string command;
    getline(cin, command);

    if (command == "SCAN") {
        scan_inputs();
    } else if (command == "CALCULATE") {
        calculate_score();
    } else {
        cerr << "Unknown command.\n";
        return 1;
    }
    return 0;
}
