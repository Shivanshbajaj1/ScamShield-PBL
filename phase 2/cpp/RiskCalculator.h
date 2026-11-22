#ifndef RISK_CALCULATOR_H
#define RISK_CALCULATOR_H
#include "Scanner.h"
#include <string>
#include <vector>

using namespace std;
class RiskCalculator {
private:
    int maximum_score;
public:
    RiskCalculator();
    int calculate(const vector<Finding> &findings);
    string label(int score);
    string reasons(const vector<Finding> &findings);
};
#endif
