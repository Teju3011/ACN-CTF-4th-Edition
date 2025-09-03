#include <stdio.h>

// fake #1: ACNCTF{ur_og_flag}
const char *data1 = "array1: ACNCTF{ur_og_flag}";

// fake #2: random junk
const char *data2 = "array2: X9z1@#%&LMNOP";

// real flag: 5-bit chunks (kept as raw text so it shows in .rdata)
const char *data3 = "array3: 01001 10111 00110 10011 10010 10001 00001 01011 10010 10110 10111";

// fake #3: more random bits
const char *data4 = "array4: 10101 01010 11100 00101 11011 01101";

// A riddle/hint, will show up as a string in the binary
volatile const char riddle[] __attribute__((used)) =
    "      Atbash Einstein ONcE said..."
    "Out of all the ENCRYPTED ROTten foods I have eaten, PIG was the most rotten. Which is why ROTten things must be ROTATED.\n";
    

void helper() {
    printf("           ALL THE BEST!!       ");
    printf("BACON is made from PORK, or a cow?");
}

int main() {
    helper();
    return 0;
}
