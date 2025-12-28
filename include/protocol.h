#ifndef PROTOCOL_H
#define PROTOCOL_H

#include <stddef.h>
#include "par.h"
#include "stats.h"

// Serialize a parsed packet into JSON.
// Returns number of bytes written.
size_t proto_packet_json(const packet_info_t* pkt, char* out, size_t max);

// Serialize a stats snapshot into JSON.
// Returns number of bytes written.
size_t proto_stats_json(const stats_snapshot_t* s, char* out, size_t max);

#endif