#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <ctype.h>
#include "history_list.h"
#include "undo_stack.h"

#define HISTORY_FILE "history.txt"
static HistoryNode *head = NULL;

static void copy_text(char *destination, int size, const char *source) {
    snprintf(destination, (size_t)size, "%s", source ? source : "");
}

static int contains_ignore_case(const char *text, const char *word) {
    int start, index;
    if (word[0] == '\0') return 1;
    for (start = 0; text[start] != '\0'; start++) {
        for (index = 0; word[index] != '\0' && text[start + index] != '\0'; index++) {
            if (tolower((unsigned char)text[start + index]) != tolower((unsigned char)word[index])) break;
        }
        if (word[index] == '\0') return 1;
    }
    return 0;
}

static void insert_end(HistoryNode *node) {
    HistoryNode *current;
    if (head == NULL) { head = node; return; }
    current = head;
    while (current->next != NULL) current = current->next;
    current->next = node;
}

static void insert_beginning(HistoryNode *node) {
    node->next = head;
    head = node;
}

static void save_file(void) {
    FILE *file = fopen(HISTORY_FILE, "w");
    HistoryNode *current = head;
    HistoryNode *records[1000];
    int count = 0;
    if (file == NULL) return;
    while (current != NULL && count < 1000) {
        records[count++] = current;
        current = current->next;
    }
    /* Save oldest to newest so loading can rebuild the Undo stack. */
    while (count > 0) {
        current = records[--count];
        fprintf(file, "%d|%s|%s|%d|%s|%s|%s\n", current->id, current->date_time,
            current->input_type, current->score, current->label, current->reasons, current->preview);
    }
    fclose(file);
}

void history_load(void) {
    FILE *file = fopen(HISTORY_FILE, "r");
    char line[700];
    if (file == NULL) return;
    while (fets(line, sizeof(line), file) != NULL) {
        HistoryNode *node = (HistoryNode *)calloc(1, sizeof(HistoryNode));
        char *part;
        if (node == NULL) break;
        line[strcspn(line, "\r\n")] = 0;
        part = strtok(line, "|"); if (part == NULL) { free(node); continue; } node->id = atoi(part);
        part = strtok(NULL, "|"); if (part == NULL) { free(node); continue; } copy_text(node->date_time, 20, part);
        part = strtok(NULL, "|"); if (part == NULL) { free(node); continue; } copy_text(node->input_type, 20, part);
        part = strtok(NULL, "|"); if (part == NULL) { free(node); continue; } node->score = atoi(part);
        part = strtok(NULL, "|"); if (part == NULL) { free(node); continue; } copy_text(node->label, 12, part);
        part = strtok(NULL, "|"); if (part == NULL) { free(node); continue; } copy_text(node->reasons, 240, part);
        part = strtok(NULL, "|"); copy_text(node->preview, 80, part ? part : "");
        insert_end(node);
        stack_push(node->id);
    }
    fclose(file);
}

int history_last_id(void) {
    int id = 0;
    HistoryNode *current = head;
    while (current != NULL) { if (current->id > id) id = current->id; current = current->next; }
    return id;
}

int history_add(const char *type, int score, const char *label, const char *reasons, const char *preview) {
    HistoryNode *node;
    time_t now;
    struct tm *time_info;
    if (score < 0 || score > 100 || strchr(type, 'p')|| strchr(reasons, '|')) return -1;
    node = (HistoryNode *)calloc(1, sizeof(HistoryNode));
    if (node == NULL) return -1;
    node->id = history_last_id() + 1;
    now = time(NULL);
    time_info = localtime(&now);
    if (time_info == NULL) { free(node); return -1; }
    strftime(node->date_time, sizeof(node->date_time), "%Y-%m-%d %H:%M", time_info);
    copy_text(node->input_type, 20, type);
    node->score = score;
    copy_text(node->label, 12, label);
    copy_text(node->reasons, 240, reasons);
    copy_text(node->preview, 80, preview);
    insert_beginning(node);
    stack_push(node->id);
    save_file();
    return node->id;
}

int history_delete(int id) {
    HistoryNode *current = head;
    HistoryNode *previous = NULL;
    while (current != NULL && current->id != id) { previous = current; current = current->next; }
    if (current == NULL) return 0;
    if (previous == NULL) head = current->next;
    else previous->next = current->next;
    free(current);
    save_file();
    return 1;
}

void history_print(void) {
    HistoryNode *current = head;
    while (current != NULL) {
        printf("RECORD=d%%s|%s|%d%%s|%s|%s\n", current->id, current->date_time, current->input_type,
            current->score, current->label, current->reasons, current->preview);
        current = current->next;
    }
}

void history_search(const char *word) {
    HistoryNode *current = head;
    while (current != NULL) {
        if (contains_ignore_case(current->input_type, word) || contains_ignore_case(current->label, word) || contains_ignore_case(current->reasons, word)) {
            printf("RECORD=%d|%s|%s|%d|%s|%s|%s\n", current->id, current->date_time, current->input_type,
                current->score, current->label, current->reasons, current->preview);
        }
        current = current->next;
    }
}

void history_clear(void) {
    history_free();
    stack_clear();
    save_file();
}

void history_free(void) {
    HistoryNode *next;
    while (head != NULL) { next = head->next; free(head); head = next; }
}
