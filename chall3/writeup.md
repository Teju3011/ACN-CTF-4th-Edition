# Easy Reverse Engineering Challenge

**Category:** Reverse Engineering\
**Difficulty:** Medium

## Description

We found a suspicious program. Can you figure out the secret key it
wants?\
Your task: analyze the file and recover the flag.

## Challenge

-   Download the file (`luckynumber3.exe`)
-   Run it using GCC/GNU commands and get the flag located somewhere in the mess.
-   Tools you might use: `strings`, GNU, MinGW.

## Flag Format

    ACNCTF{...}


**Author's Note:** This is a easy-to-medium level reversing challenge. Good luck!





.







.






.








.




 

.







.






.








.
## Solution


1. first of all, luckynumber3 is downloaded and then run using MinGW using command either

    `objdump -s luckynumber3.exe`

    OR

    `objdump -s -j .rdata luckynumber3.exe`
   
3. somewhere around _memory address_ **14000b000**, .rdata will start, where 4 arrays can be seen.
4. after the arrays, some other text is seen, those are the riddles to identify with what ciphertext the flag has been encrypted.
5. ofc, **array3** is the correct flag, rest all are dummies.{mentioned in the .exe filename that important number is 3}
6. order of encryption was _Atbash<<ROT13 WITH ROTATION of NUMBERS<<Bacon._ , so decryption will be opposite.
7. finally, the decoded flag obtained from the .exe file is
                                  `ACNCTF{CONGPATULATIONS}`
