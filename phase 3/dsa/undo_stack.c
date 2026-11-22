#include <stdlib.h>
#include "undo_stack.h"

typedef struct StackNode {
    int id;
    struct StackNode *next;
} StackNode;

static StackNode *top = NULL;

void stack_push(int id) {
    StackNode *node = (StackNode *)malloc(sizeof(StackNode));
    if (node == NULL) return;
    node->id = id;
    node->next = top;
    top = node;
}

int stack_pop(void) {
    StackNode *node;
    int id;
    if (top == NULL) return -1;
    node = top;
    id = node->id;
    top = top->next;
    free(node);
    return id;
}

void stack_clear(void) {
    while (stack_pop() != -1) { }
}
