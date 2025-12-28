#include "stats.h"
#include "util.h"
#include "par.h"
#include <string.h>


static uint64_t last_time = 0;
static uint64_t bytes_down = 0;
static uint64_t bytes_up = 0;

static uint64_t tcp = 0, udp = 0, icmp = 0;
static uint64_t total = 0;

void stats_init(void) {
    last_time = util_timestamp_ns();
}

void stats_update(const packet_info_t* pkt) {
    total++;

    switch (pkt->protocol) {
        case 6: tcp++; break;
        case 17: udp++; break;
        case 1: icmp++; break;
    }

    // TODO: Determine direction (up/down)
    bytes_down += pkt->length;
}

void stats_get(stats_snapshot_t* out) {
    memset(out, 0, sizeof(*out));

    uint64_t now = util_timestamp_ns();
    double seconds = (now - last_time) / 1e9;

    out->mbps_down = (bytes_down * 8.0) / (seconds * 1e6);
    out->mbps_up   = (bytes_up   * 8.0) / (seconds * 1e6);

    out->total_packets = total;
    out->tcp_count = tcp;
    out->udp_count = udp;
    out->icmp_count = icmp;

    // Reset counters for next interval
    bytes_down = bytes_up = 0;
    last_time = now;
}