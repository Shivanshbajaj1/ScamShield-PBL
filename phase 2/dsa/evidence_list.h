#ifndef EVIDENCE_LIST_H
#define EVIDENCE_LIST_H

typedef struct EvidenceRecord {
    char name[40];
    char reason[160];
    int points;
} EvidenceRecord;

void evidenceInsertEnd(const char *name, const char *reason, int points);
int evidenceCount(void);
int evidenceGet(int position, EvidenceRecord *record);
int evidenceSearch(const char *name);
void evidenceDisplay(void);
void evidenceClear(void);

#endif
