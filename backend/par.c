#include "par.h"
#include "util.h"
#include <string.h>

int par_parse(const uint8_t* data, size_t len, packet_info_t* out) {
    if (len < 34) return -1; // too small for Ethernet + IP

    memset(out, 0, sizeof(*out));
    out->timestamp = util_timestamp_ns();
    out->length = len;

    // TODO: Parse Ethernet header
    // TODO: Parse IPv4 header
    // TODO: Parse TCP/UDP headers

    return 0;
}