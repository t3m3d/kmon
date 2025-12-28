#include "util.h"
#include <windows.h>
#include <stdio.h>

uint64_t util_timestamp_ns(void) {
    LARGE_INTEGER freq, counter;
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&counter);
    return (uint64_t)((counter.QuadPart * 1000000000ULL) / freq.QuadPart);
}

const char* util_ip_to_str(uint32_t ip) {
    static char buf[32];
    sprintf(buf, "%u.%u.%u.%u",
        (ip & 0xFF),
        (ip >> 8) & 0xFF,
        (ip >> 16) & 0xFF,
        (ip >> 24) & 0xFF
    );
    return buf;
}