// keyed_rotate_hard.c
// Hard Linux x64 reverse challenge
// Obfuscation: split enc arrays, computed key, opaque predicates, anti-debug checks.
// Flag (decrypted at runtime): ACNCTF{wh0s_y0ur_dec0mp1ler_n0w}

#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include <stdlib.h>
#include <fcntl.h>
#include <stdbool.h>

static uint32_t compute_hash(const char *s) {
    uint32_t h = 0x1337;
    for (size_t i = 0; i < strlen(s); ++i) {
        // rotate-left by 3 within 32-bit and xors
        h = ( (h << 3) | (h >> (29)) ) ^ (unsigned char)s[i];
        h = (h + (uint32_t)(i * 0x9)) & 0xFFFFFFFF;
        // tiny opaque op
        if ((h ^ 0xdeadbeef) < 10) h ^= 0xabcdef;
    }
    return h;
}

/* The encryption used (creator side):
   enc[i] = ((flag[i] + i) ^ key[i % 5]) & 0xff

   Decrypt with: flag[i] = ((enc[i] ^ key[i%5]) - i) & 0xff
*/

/* split encrypted bytes into pieces to make static analysis more annoying */
static const unsigned char enc_part_a[] = {
    0x53,0x70,0x06,0x3e,0xc2,0x59,0xb5,0x28,0x08,0xa3
};
static const unsigned char enc_part_b[] = {
    0x6f,0x5e,0xd3,0x45,0x19,0x93,0x5b,0x23,0x0f,0xec
};
static const unsigned char enc_part_c[] = {
    0x56,0xb6,0xd0,0x30,0x1e,0x6c,0xb8,0x2c,0xf2,0xd7,0x87,0xa8
};
/* total length: 33 bytes */

/* produce the key dynamically (obfuscated arithmetic) */
static void produce_key(unsigned char out[5]) {
    /* generate [0x12,0x34,0x56,0x78,0x9a] by nontrivial ops */
    unsigned int a = (0x24 >> 1);                 // 0x12
    unsigned int b = (0x68 >> 1);                 // 0x34
    unsigned int c = (0xac >> 2) + 0x0a;          // 0x56
    unsigned int d = (0x1e0 >> 2) + 0x10;         // 0x78
    unsigned int e = (0x1f4 >> 2) + 0x14;         // 0x9a
    out[0] = (unsigned char)(a & 0xFF);
    out[1] = (unsigned char)(b & 0xFF);
    out[2] = (unsigned char)(c & 0xFF);
    out[3] = (unsigned char)(d & 0xFF);
    out[4] = (unsigned char)(e & 0xFF);

    /* tiny opaque predicate to confuse decompilers */
    if ((out[0] + out[1] + out[2]) % 3 == 0) {
        volatile int junk = 0;
        for (int i = 0; i < 3; ++i) { junk += i; }
    } else {
        asm volatile("nop");
    }
}

/* light anti-debug using ptrace and /proc/self/status TracerPid check */
static bool anti_debug(void) {
    /* ptrace: if being traced, PTRACE_TRACEME returns -1 */
    if (ptrace(PTRACE_TRACEME, 0, 0, 0) == -1) {
        return true;
    }
    /* check /proc/self/status TracerPid */
    int fd = open("/proc/self/status", O_RDONLY);
    if (fd >= 0) {
        char buf[512];
        ssize_t r = read(fd, buf, sizeof(buf)-1);
        close(fd);
        if (r > 0) {
            buf[r] = 0;
            const char *p = strstr(buf, "TracerPid:");
            if (p) {
                int tracer = atoi(p + 10);
                if (tracer != 0) return true;
            }
        }
    }
    return false;
}

/* decrypts into out (must be at least 34 bytes) */
static void decrypt_flag(unsigned char *out, size_t n) {
    unsigned char key[5];
    produce_key(key);

    unsigned char enc[64];
    size_t p1 = sizeof(enc_part_a);
    size_t p2 = sizeof(enc_part_b);
    size_t p3 = sizeof(enc_part_c);
    memset(enc, 0, sizeof(enc));
    memcpy(enc, enc_part_a, p1);
    memcpy(enc + p1, enc_part_b, p2);
    memcpy(enc + p1 + p2, enc_part_c, p3);

    for (size_t i = 0; i < n; ++i) {
        /* decrypt: flag[i] = ((enc[i] ^ key[i%5]) - i) & 0xff */
        unsigned char v = (unsigned char)((enc[i] ^ key[i % 5]));
        out[i] = (unsigned char)((v - (unsigned char)i) & 0xff);
        /* small anti-analysis jitter */
        if ((i & 3) == 0) asm volatile("nop");
    }
    out[n] = 0;
    /* zero sensitive local copy */
    memset(enc, 0, sizeof(enc));
}

/* small noisy function (control-flow clutter) */
static int perplex(int x) {
    if ((x * 7) % 13 == 0) return x ^ 0xAA;
    if ((x * 3) % 7 == 0) return x ^ 0x55;
    // rarely taken branch that confuses decompiler
    if (x == 0x1337) {
        volatile int j = 0;
        for (int i = 0; i < 5; ++i) j += i;
        return j;
    }
    return x;
}

int main(void) {
    /* anti-debug; if detected, do a misleading behavior and exit */
    if (anti_debug()) {
        puts("Service unavailable. Try again later.");
        return 0;
    }

    char buf[128];
    printf("Enter secret: ");
    if (!fgets(buf, sizeof(buf), stdin)) return 0;
    buf[strcspn(buf, "\n")] = 0;

    /* small confusing op before hash */
    (void)perplex(0x123);

    uint32_t hv = compute_hash(buf);
    /* target is obfuscated by arithmetic rather than literal */
    uint32_t target = (0x4f * 0x1000000u) | (0x09 * 0x10000u) | (0xcb * 0x100u) | 0x3e;
    if (hv == target) {
        unsigned char flagbuf[64];
        decrypt_flag(flagbuf, 33); /* 33 bytes long */
        printf("Correct! Flag: %s\n", flagbuf);
        /* zero flag memory after printing to reduce easy static leaks */
        memset(flagbuf, 0, sizeof(flagbuf));
    } else {
        puts("Nope.");
    }
    return 0;
}
