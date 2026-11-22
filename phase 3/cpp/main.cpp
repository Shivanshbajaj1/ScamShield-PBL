#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include "Scanner.h"
#include "RiskCalculator.h"

using namespace std;

static void scan_inputs(const string &text, const vector<string> &urls) {
    vector<Finding> findings;
    MessageScanner message_scanner;
    URLScanner url_scanner;
    Scanner *scanner;

    if (!text.empty()) {
        scanner = &message_scanner;
        scanner->scan(text, findings);
    }

    scanner = &url_scanner;
    for (size_t index = 0; index < urls.size(); index++) {
        if (!urls[index].empty()) scanner->scan(urls[index], findings);
    }

    /* Python sends these findings to the C evidence linked list for deduplication. */
    for (const Finding &item : findings) {
        cout << "FINDING=" << item.name << "|" << item.reason << "|" << item.points << "\n";
    }
}

static void calculate_score(int count) {
    vector<Finding> findings;
    string name, reason, points_text;
    for (int index = 0; index < count; index++) {
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

    if (command == "SCAN_MULTI" || command == "SCAN") {
        string type, text, count_text, url;
        vector<string> urls;
        getline(cin, type);
        getline(cin, text);

        if (command == "SCAN") {
            getline(cin, url);
            if (!url.empty()) urls.push_back(url);
        } else {
            getline(cin, count_text);
            int count = atoi(count_text.c_str());
            if (count < 0 || count > 100) {
                cerr << "Invalid URL count. Maximum is 100.\n";
                return 1;
            }
            for (int index = 0; index < count; index++) {
                getline(cin, url);
                if (!url.empty()) urls.push_back(url);
            }
        }

        if (text.empty() && urls.empty()) {
            cerr << "Enter at least one input before scanning.\n";
            return 1;
        }
        scan_inputs(text, urls);
    } else if (command == "CALCULATE") {
        string count_text;
        getline(cin, count_text);
        int count = atoi(count_text.c_str());
        if (count < 0 || count > 500) {
            cerr << "Invalid finding count.\n";
            return 1;
        }
        calculate_score(count);
    } else {
        cerr << "Unknown scanner command.\n";
        return 1;
    }
    return 0;
}
