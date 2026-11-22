#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "history_list.h"
#include "undo_stack.h"
#include "evidence_list.h"

static void read_line(char *text, int size) {
    if (fgets(text, size, stdin) == NULL) text[0] = '\0';
    text[strcspn(text, "\r\n")] = '\0';
}

static void finish(void) {
    history_free();
    stack_clear();
    evidenceClear();
}

int main(void) {
    char command[40];
    char type[40], score_text[30], label[20], reasons[500], preview[200], word[200];
    read_line(command, sizeof(command));

    if (strcmp(command, "EVIDENCE") == 0) {
        char count_text[30], name[100], reason[300], points_text[30];
        int count, index;
        EvidenceRecord record;
        read_line(count_text, sizeof(count_text));
        count = atoi(count_text);
        if (count < 0 || count > 500) return 1;
        for (index = 0; index < count; index++) {
            read_line(name, sizeof(name));
            read_line(reason, sizeof(reason));
            read_line(points_text, sizeof(points_text));
            evidenceInsertEnd(name, reason, atoi(points_text));
        }
        for (index = 0; index < evidenceCount(); index++) {
            if (evidenceGet(index, &record)) {
                printf("FINDING=%s|%s|%d\n", record.name, record.reason, record.points);
            }
        }
        evidenceClear();
        return 0;
    }

    history_load();

    if (strcmp(command, "ADD") == 0) {
        int id;
        read_line(type, sizeof(type));
        read_line(score_text, sizeof(score_text));
        read_line(label, sizeof(label));
        read_line(reasons, sizeof(reasons));
        read_line(preview, sizeof(preview));
        id = history_add(type, atoi(score_text), label, reasons, preview);
        if (id < 0) { finish(); return 1; }
        printf("ID=%d\n", id);
    } else if (strcmp(command, "LIST") == 0) {
        history_print();
    } else if (strcmp(command, "SEARCH") == 0) {
        read_line(word, sizeof(word));
        history_search(word);
    } else if (strcmp(command, "UNDO") == 0) {
        int id = stack_pop();
        if (id < 0 || !history_delete(id)) printf("UNDO=EMPTY\n");
        else printf("UNDO=%d\n", id);
    } else if (strcmp(command, "CLEAR") == 0) {
        history_clear();
        printf("CLEAR=OK\n");
    } else {
        finish();
        fprintf(stderr, "Unknown DSA command.\n");
        return 1;
    }

    finish();
    return 0;
}
