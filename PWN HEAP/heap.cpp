/* heap_simulated_pwn.c
   Safe simulated heap "overflow" challenge for CTF use.
   - No undefined behavior, no gets()/unsafe scanf.
   - Players must craft input LONG_ENOUGH or include magic substring to "simulate" overflow.
   - Compile: gcc -O2 -std=c11 -o heap_simulated_pwn heap_simulated_pwn.c
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FLAGSIZE_MAX 64
#define INPUT_DATA_SIZE 5
#define SAFE_VAR_SIZE 16


char *safe_var;
char *input_data;

void check_win() {
    if (strcmp(safe_var, "overflowed") == 0) {
        printf("\nYOU WIN\n");
        char buf[FLAGSIZE_MAX];
        FILE *fd = fopen("flag.txt", "r");
        if (fd) {
            if (fgets(buf, FLAGSIZE_MAX, fd)) {
                printf("%s\n", buf);
            } else {
                printf("flag file is empty or unreadable\n");
            }
            fclose(fd);
        } else {
            printf("flag file not found\n");
        }
        fflush(stdout);
        exit(0);
    } else {
        printf("Looks like everything is still secure!\n");
        printf("\nACNCTF{U_still_need_to_exploit_try_again}\n");
        fflush(stdout);
    }
}

void print_menu() {
    printf("\n1. Print values"
           "\n2. Write to buffer"
           "\n3. Print safe_var"
           "\n4. Print Flag"
           "\n5. Exit\n\nEnter your choice: ");
    fflush(stdout);
}

void init() {
    printf("\nWelcome to ACN ...A easy challenge for you  !!!\n The key to open the flag is overflowed");
    fflush(stdout);

    
    input_data = malloc(INPUT_DATA_SIZE);
    if (!input_data) { perror("malloc"); exit(1); }
  
    memset(input_data, 0, INPUT_DATA_SIZE);
    strncpy(input_data, "J3$T3R", INPUT_DATA_SIZE - 1);

    safe_var = malloc(SAFE_VAR_SIZE);
    if (!safe_var) { perror("malloc"); exit(1); }
    memset(safe_var, 0, SAFE_VAR_SIZE);
    strncpy(safe_var, "secure", SAFE_VAR_SIZE - 1);
}

void write_buffer() {
    char tmp[512];
    printf("Data for buffer: ");
    fflush(stdout);

    if (!fgets(tmp, sizeof(tmp), stdin)) {
        printf("\nInput error\n");
        return;
    }
    tmp[strcspn(tmp, "\n")] = '\0';

    size_t len = strlen(tmp);
    strcpy(input_data, tmp);
    input_data[INPUT_DATA_SIZE - 1] = '\0';
    printf("I hope still my input variable is fine but I have a strong feeling that while eating STRacciatella Cofy i made a bug  ....if u found it...U would be rewarded a bounty")
    fflush(stdout);
}

void print_heap() {
    printf("Heap State:\n");
    printf("+----------------------+----------------+\n");
    printf("[*] Address (heap)  ->   Heap Data   \n");
    printf("+----------------------+----------------+\n");
    printf("[*]   %p  ->   %s\n", (void *)input_data, input_data);
    printf("+----------------------+----------------+\n");
    printf("[*]   %p  ->   %s\n", (void *)safe_var, safe_var);
    printf("+----------------------+----------------+\n");
    fflush(stdout);
}

int main(void) {
    init();
    print_heap();

    while (1) {
        print_menu();
        int choice;
        int rval = scanf("%d", &choice);
        if (rval == EOF) {
            printf("\nbye\n");
            exit(0);
        }
        if (rval != 1) {
           
            char c; while ((c = getchar()) != '\n' && c != EOF);
            printf("Invalid input. Exiting.\n");
            exit(0);
        }

        char ch = getchar();
        if (ch != '\n' && ch != EOF) { 
            ungetc(ch, stdin);
        }

        switch (choice) {
            case 1:
                print_heap();
                break;
            case 2:
                write_buffer();
                break;
            case 3:
                printf("\n\nTake a look at my variable: safe_var = %s\n\n", safe_var);
                fflush(stdout);
                break;
            case 4:
                check_win();
                break;
            case 5:
                return 0;
            default:
                printf("Invalid choice\n");
                fflush(stdout);
        }
    }


    return 0;
}

