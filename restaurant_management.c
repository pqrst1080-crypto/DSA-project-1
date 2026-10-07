#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX 20
#define MAX_ITEMS 5

/* ---------- MENU ITEM ---------- */

typedef struct {
    int id;
    char name[30];
    float price;
} MenuItem;


/* ---------- ORDER ---------- */

typedef struct {
    int id;
    char customer[30];
    MenuItem items[MAX_ITEMS];
    int itemCount;
    float total;
} Order;


/* =========================================
   MODULE 1: STACK
   Used to undo the last order
========================================= */

typedef struct {
    Order data[MAX];
    int top;
} Stack;

void push(Stack *s, Order order) {
    if (s->top < MAX - 1)
        s->data[++s->top] = order;
}

int pop(Stack *s, Order *order) {
    if (s->top == -1)
        return 0;

    *order = s->data[s->top--];
    return 1;
}


/* =========================================
   MODULE 1: QUEUE
   Used for kitchen orders (FIFO)
========================================= */

typedef struct {
    Order data[MAX];
    int front;
    int rear;
} Queue;

void enqueue(Queue *q, Order order) {
    if (q->rear < MAX - 1)
        q->data[++q->rear] = order;
}

int dequeue(Queue *q, Order *order) {
    if (q->front > q->rear)
        return 0;

    *order = q->data[q->front++];
    return 1;
}


/* =========================================
   MODULE 2: LINKED LIST
   Used for billing history
========================================= */

typedef struct Node {
    Order order;
    struct Node *next;
} Node;

Node *head = NULL;

void addHistory(Order order) {

    Node *newNode = (Node *)malloc(sizeof(Node));

    newNode->order = order;
    newNode->next = NULL;

    if (head == NULL) {
        head = newNode;
    } else {

        Node *temp = head;

        while (temp->next != NULL)
            temp = temp->next;

        temp->next = newNode;
    }
}


/* =========================================
   MODULE 3: BST
   Used to store menu items by price
========================================= */

typedef struct BSTNode {

    MenuItem item;

    struct BSTNode *left;
    struct BSTNode *right;

} BSTNode;

BSTNode *root = NULL;

BSTNode *createNode(MenuItem item) {

    BSTNode *newNode = (BSTNode *)malloc(sizeof(BSTNode));

    newNode->item = item;
    newNode->left = NULL;
    newNode->right = NULL;

    return newNode;
}

BSTNode *insertBST(BSTNode *root, MenuItem item) {

    if (root == NULL)
        return createNode(item);

    if (item.price < root->item.price)
        root->left = insertBST(root->left, item);
    else
        root->right = insertBST(root->right, item);

    return root;
}

void displayMenu(BSTNode *root) {

    if (root != NULL) {

        displayMenu(root->left);

        printf("[%d] %-20s Rs. %.2f\n",
               root->item.id,
               root->item.name,
               root->item.price);

        displayMenu(root->right);
    }
}


/* =========================================
   MODULE 4: MERGE SORT
   Used to sort bills by total
========================================= */

void merge(Order arr[], int left, int mid, int right) {

    int n1 = mid - left + 1;
    int n2 = right - mid;

    Order L[MAX], R[MAX];

    int i, j, k;

    for (i = 0; i < n1; i++)
        L[i] = arr[left + i];

    for (j = 0; j < n2; j++)
        R[j] = arr[mid + 1 + j];

    i = 0;
    j = 0;
    k = left;

    while (i < n1 && j < n2) {

        if (L[i].total <= R[j].total)
            arr[k++] = L[i++];
        else
            arr[k++] = R[j++];
    }

    while (i < n1)
        arr[k++] = L[i++];

    while (j < n2)
        arr[k++] = R[j++];

}

void mergeSort(Order arr[], int left, int right) {

    if (left < right) {

        int mid = (left + right) / 2;

        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);

        merge(arr, left, mid, right);
    }
}


/* =========================================
   DISPLAY ORDER
========================================= */

void displayOrder(Order order) {

    printf("\nOrder #%d\n", order.id);
    printf("Customer: %s\n", order.customer);

    printf("Items: ");

    for (int i = 0; i < order.itemCount; i++) {

        printf("%s", order.items[i].name);

        if (i < order.itemCount - 1)
            printf(", ");
    }

    printf("\nTotal: Rs. %.2f\n", order.total);
}


/* =========================================
   MAIN PROGRAM
========================================= */

int main() {

    /* Default Menu */

    MenuItem menu[] = {

        {1, "Burger", 120},
        {2, "Pizza", 250},
        {3, "Juice", 50},
        {4, "Pasta", 180},
        {5, "Ice Cream", 80}

    };

    int menuCount = 5;

    /* Create BST */

    for (int i = 0; i < menuCount; i++)
        root = insertBST(root, menu[i]);


    /* Initialize Stack */

    Stack stack;
    stack.top = -1;


    /* Initialize Queue */

    Queue queue;
    queue.front = 0;
    queue.rear = -1;


    int choice;
    int orderId = 1;


    while (1) {

        printf("\n====================================");
        printf("\n RESTAURANT MANAGEMENT SYSTEM");
        printf("\n====================================\n");

        printf("1. View Menu\n");
        printf("2. Place Order\n");
        printf("3. Serve Next Order\n");
        printf("4. Undo Last Order\n");
        printf("5. View Sorted Bills\n");
        printf("0. Exit\n");

        printf("\nEnter choice: ");
        scanf("%d", &choice);


        /* ---------- VIEW MENU ---------- */

        if (choice == 1) {

            printf("\n----- MENU -----\n");

            displayMenu(root);
        }


        /* ---------- PLACE ORDER ---------- */

        else if (choice == 2) {

            Order order;

            order.id = orderId++;

            printf("\nCustomer name: ");
            scanf(" %[^\n]", order.customer);

            printf("How many items? ");
            scanf("%d", &order.itemCount);

            order.total = 0;

            displayMenu(root);

            for (int i = 0; i < order.itemCount; i++) {

                int id;

                printf("Enter Item ID: ");
                scanf("%d", &id);

                if (id >= 1 && id <= menuCount) {

                    order.items[i] = menu[id - 1];

                    order.total += menu[id - 1].price;

                } else {

                    printf("Invalid ID!\n");

                    i--;
                }
            }


            /* Add to Queue */

            enqueue(&queue, order);


            /* Add to Stack */

            push(&stack, order);


            printf("\nOrder placed successfully!\n");

            displayOrder(order);
        }


        /* ---------- SERVE ORDER ---------- */

        else if (choice == 3) {

            Order order;

            if (dequeue(&queue, &order)) {

                printf("\nServing Order...\n");

                displayOrder(order);


                /* Add to Linked List */

                addHistory(order);

            } else {

                printf("\nNo pending orders.\n");
            }
        }


        /* ---------- UNDO LAST ORDER ---------- */

        else if (choice == 4) {

            Order order;

            if (pop(&stack, &order)) {

                printf("\nLast order cancelled!\n");

                displayOrder(order);

            } else {

                printf("\nNo order to undo.\n");
            }
        }


        /* ---------- VIEW SORTED BILLS ---------- */

        else if (choice == 5) {

            Order bills[MAX];

            int count = 0;

            Node *temp = head;


            /* Copy Linked List into Array */

            while (temp != NULL) {

                bills[count++] = temp->order;

                temp = temp->next;
            }


            if (count == 0) {

                printf("\nNo served orders yet.\n");

            } else {

                /* Merge Sort */

                mergeSort(bills, 0, count - 1);

                printf("\n----- SORTED BILLS -----\n");

                for (int i = 0; i < count; i++)
                    displayOrder(bills[i]);
            }
        }


        /* ---------- EXIT ---------- */

        else if (choice == 0) {

            printf("\nThank you! Goodbye!\n");

            break;
        }


        else {

            printf("\nInvalid choice!\n");
        }
    }

    return 0;
}