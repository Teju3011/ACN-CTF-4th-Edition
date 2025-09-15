/*
   format_leak_hard.c — Harder format string memory leak challenge.
   Compile: gcc -o format_leak_hard format_leak_hard.c -no-pie -fno-stack-protector
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "header.h"

char *heap_flag = NULL;


void vulnerable_echo() {
    char input[256];
    char input1[12];
    printf("Enter your input: ");
    fflush(stdout);
    if (!fgets(input, sizeof(input), stdin)) {
        puts("Input error");
        exit(1);
    }

    input[strcspn(input, "\n")] = '\0';
   
    printf(input);   
    puts("");
    printf("What you found follow the command -->  \n");
     fflush(stdout);
    if (!fgets(input1, sizeof(input1), stdin)) {
        puts("Input error");
        exit(1);
    }
    input1[strcspn(input1, "\r\n")] = '\0';
    if(strcmp(input1,KEY_FOR)==0){
    callme_when_understood();}
    
   

}   




int main() {
   

    puts("Welcome to ACN CTF — can you format your way to the flag? \n Understand the description of the Challenge its more important to WINNN");
    vulnerable_echo();
    
    

    return 0;
}
