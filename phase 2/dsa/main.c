#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "evidence_list.h"

static void read_line(char *text, int size) {
    if (fgets(text, size, stdin) == NULL) text[0] = '\0';
    text[strcspn(text, "\r\n")] = '\0';
}


int main(void) {
    char command[40], count_text[30];
    char name[100], reason[300], points_text[30];
    int count, i;
    EvidenceRecord record;

    read_line(command, sizeof(command));
    if (strcmp(command, "EVIDENCE") != 0) {
        fprintf(stderr, "Unknown DSA command.\n");
        return 1;
    }

    read_line(count_text, sizeof(count_text));
    count = atoi(count_text);

    for (i = 0; i < count; i++) {
        read_line(name, sizeof(name));
        read_line(reason, sizeof(reason));
        read_line(points_text, sizeof(points_text));
        evidenceInsertEnd(name, reason, atoi(points_text));   /* duplicates are skipped */
    }

    for (i = 0; i < evidenceCount(); i++) {
        if (evidenceGet(i, &record)) {
            printf("FINDING=%s|%s|%d\n", record.name, record.reason, record.points);
        }
    }

    evidenceClear();   /* free every node */
    return 0;
}
