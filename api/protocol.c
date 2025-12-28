#include "protocol.h"
#include "par.h"
#include "stats.h"
#include "util.h"
#include <stdio.h>

size_t proto_packet_json(const packet_info_t* pkt, char* out, size_t max) {
    return snprintf(out, max,
        "{\"type\":\"packet\",\"data\":{"
        "\"timestamp\":%llu,"
        "\"src_ip\":\"%s\","
        "\"dst_ip\":\"%s\","
        "\"src_port\":%u,"
        "\"dst_port\":%u,"
        "\"protocol\":%u,"
        "\"length\":%zu"
        "}}\n",
        pkt->timestamp,
        util_ip_to_str(pkt->src_ip),
        util_ip_to_str(pkt->dst_ip),
        pkt->src_port,
        pkt->dst_port,
        pkt->protocol,
        pkt->length
    );
}

size_t proto_stats_json(const stats_snapshot_t* s, char* out, size_t max) {
    return snprintf(out, max,
        "{\"type\":\"stats\",\"data\":{"
        "\"mbps_down\":%.3f,"
        "\"mbps_up\":%.3f,"
        "\"total_packets\":%llu,"
        "\"tcp\":%llu,"
        "\"udp\":%llu,"
        "\"icmp\":%llu"
        "}}\n",
        s->mbps_down,
        s->mbps_up,
        s->total_packets,
        s->tcp_count,
        s->udp_count,
        s->icmp_count
    );
}