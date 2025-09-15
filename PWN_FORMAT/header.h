#ifndef FLAG_H
#define FLAG_H
#define KEY_FOR "FAKEFLAG"


#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <inttypes.h>


 void (*jumper)(void);
 
void callme_when_understood(void) {
    char buf[64];
    unsigned long long val;
    char *end;

    printf("Enter address to for the pointer (hex, e.g. 0x401080): ");
    fflush(stdout);

    if (!fgets(buf, sizeof buf, stdin)) {
        puts("input error");
        return;
    }

    /* trim newline */
    buf[strcspn(buf, "\n")] = '\0';

    errno = 0;
    val = strtoull(buf, &end, 0); /* base 0 accepts 0x... or decimal */
    if (end == buf) {
        puts("no number supplied");
        return;
    }
    if (errno == ERANGE) {
        puts("value out of range");
        return;
    }

    /* Optionally: add range checks here */
    jumper = (void(*)(void))(uintptr_t)val;
    if (jumper) jumper();
}



#define FLAGSIZE_MAX 64
const char hidden_flag[] =  "\x74\x79\x70\x65\x5f\x46\x41\x4b\x45\x46\x4c\x41\x47";

void WINNN(){
	printf("\nYOU found my hint and found J3$T3R real WINNN...\n");
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
        return ;
}
#endif
