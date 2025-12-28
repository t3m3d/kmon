#ifndef UTIL_H
#define UTIL_H

#include <stdint.h>

uint64_t util_timestamp_ns(void);
const char* util_ip_to_str(uint32_t ip);

#endif