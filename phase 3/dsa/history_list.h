#ifndef HISTORY_LIST_H
#define HISTORY_LIST_H

typedef struct HistoryNode {
    int id;
    char date_time[20];
    char input_type[20];
    int score;
    char label[12];
    char reasons[240];
    char preview[80];
    struct HistoryNode *next;
} HistoryNode;

void history_load(void);
int history_add(const char *type, int score, const char *label, const char *reasons, const char *preview);
int history_delete(int id);
void history_print(void);
void history_search(const char *word);
void history_clear(void);
int history_last_id(void);
void history_free(void);

#endif
