#include "RiskCalculator.h"

using namespace std;
RiskCalculator::RiskCalculator() { maximum_score = 100; }
int RiskCalculator::calculate(const vector<Finding> &findings) { int score = 0; for (const Finding &item : findings) score += item.points; return score > maximum_score ? maximum_score : score; }
string RiskCalculator::label(int score) { if (score >= 60) return "Scam"; if (score >= 30) return "Suspicious"; return "Safe"; }
string RiskCalculator::reasons(const vector<Finding> &findings) { string text; for (const Finding &item : findings) { if (!text.empty()) text += "; "; text += item.reason; } return text.empty() ? "No configured warning signs" : text; }
