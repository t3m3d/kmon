#ifndef PAR_H
#define PAR_H

#include <stdint.h>
#include <stddef.h>

// Parsed packet structure
typedef struct {
    uint64_t timestamp;
    uint32_t src_ip;
    uint32_t dst_ip;
    uint16_t src_port;
    uint16_t dst_port;
    uint8_t protocol;   // TCP=6, UDP=17, ICMP=1, etc.
    size_t length;
} packet_info_t;

int par_parse(const uint8_t* data, size_t len, packet_info_t* out);

#endif