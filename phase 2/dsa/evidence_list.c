#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "evidence_list.h"

typedef struct EvidenceNode {
    EvidenceRecord data;
    struct EvidenceNode *next;
} EvidenceNode;

static EvidenceNode *evidenceHead = NULL;

int evidenceSearch(const char *name) {
    EvidenceNode *temp = evidenceHead;
    while (temp != NULL) {
        if (strcmp(temp->data.name, name) == 0) return 1;
        temp = temp->next;
    }
    return 0;
}

void evidenceInsertEnd(const char *name, const char *reason, int points) {
    EvidenceNode *newNode;
    EvidenceNode *temp;
    if (evidenceSearch(name)) return;
    newNode = (EvidenceNode *)malloc(sizeof(EvidenceNode));
    if (newNode == NULL) return;
    snprintf(newNode->data.name, sizeof(newNode->data.name), "%s", name);
    snprintf(newNode->data.reason, sizeof(newNode->data.reason), "%s", reason);
    newNode->data.points = points;
    newNode->next = NULL;
    if (evidenceHead == NULL) {
        evidenceHead = newNode;
        return;
    }
    temp = evidenceHead;
    while (temp->next != NULL) temp = temp->next;
    temp->next = newNode;
}

int evidenceCount(void) {
    int count = 0;
    EvidenceNode *temp = evidenceHead;
    while (temp != NULL) { count++; temp = temp->next; }
    return count;
}

int evidenceGet(int position, EvidenceRecord *record) {
    int index = 0;
    EvidenceNode *temp = evidenceHead;
    while (temp != NULL) {
        if (index == position) { *record = temp->data; return 1; }
        index++;
        temp = temp->next;
    }
    return 0;
}

void evidenceDisplay(void) {
    int index = 0;
    EvidenceRecord record;
    while (evidenceGet(index, &record)) {
        printf("EVIDENCE=%s|%s|%d\n", record.name, record.reason, record.points);
        index++;
    }
}

void evidenceClear(void) {
    EvidenceNode *temp;
    while (evidenceHead != NULL) {
        temp = evidenceHead;
        evidenceHead = evidenceHead->next;
        free(temp);
    }
}
