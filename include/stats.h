#ifndef STATS_H
#define STATS_H

#include "par.h"
#include <stdint.h>

typedef struct {
    double mbps_down;
    double mbps_up;
    uint64_t total_packets;
    uint64_t tcp_count;
    uint64_t udp_count;
    uint64_t icmp_count;
} stats_snapshot_t;

void stats_init(void);
void stats_update(const packet_info_t* pkt);
void stats_get(stats_snapshot_t* out);

#endif