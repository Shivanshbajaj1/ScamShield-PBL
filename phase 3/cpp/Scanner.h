#ifndef SCANNER_H
#define SCANNER_H
#include <string>
#include <vector>

using namespace std;

struct Finding { string name; string reason; int points; };

class Scanner {
private:
    string scanner_name;
public:
    Scanner(const string &name);
    virtual ~Scanner() {}
    string name() const;
    virtual void scan(const string &input, vector<Finding> &findings) = 0;
};

class MessageScanner : public Scanner {
public:
    MessageScanner();
    void scan(const string &input, vector<Finding> &findings) override;
};

class URLScanner : public Scanner {
public:
    URLScanner();
    void scan(const string &input, vector<Finding> &findings) override;
};

void add_finding(vector<Finding> &findings, const string &name, const string &reason, int points);
#endif
