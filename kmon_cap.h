// kmon_cap.h — C bridge for libpcap packet capture
// Only the parts that need C: callback, byte arrays, hex encoding
// Byte/U16/U32 parsing is now done in pure Krypton (kmon_utils.k)

#ifndef KMON_CAP_H
#define KMON_CAP_H

#include <pcap.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#define KMON_MAX_PKT_LEN 65536
#define KMON_PKT_QUEUE   64

typedef struct {
    uint8_t  data[KMON_MAX_PKT_LEN];
    uint32_t len;
    uint64_t ts_ns;
} kmon_packet_t;

static pcap_t*       kmon_handle = NULL;
static kmon_packet_t kmon_queue[KMON_PKT_QUEUE];
static int           kmon_qhead  = 0;
static int           kmon_qtail  = 0;

static void kmon_cap_handler(u_char* user, const struct pcap_pkthdr* hdr, const u_char* pkt) {
    int next = (kmon_qtail + 1) % KMON_PKT_QUEUE;
    if (next == kmon_qhead) return;
    uint32_t cplen = hdr->len < KMON_MAX_PKT_LEN ? hdr->len : KMON_MAX_PKT_LEN;
    memcpy(kmon_queue[kmon_qtail].data, pkt, cplen);
    kmon_queue[kmon_qtail].len   = cplen;
    kmon_queue[kmon_qtail].ts_ns = (uint64_t)hdr->ts.tv_sec * 1000000000ULL
                                 + (uint64_t)hdr->ts.tv_usec * 1000ULL;
    kmon_qtail = next;
}

static char* kmonCapOpen(const char* iface) {
    char errbuf[PCAP_ERRBUF_SIZE];
    kmon_handle = pcap_open_live(iface, KMON_MAX_PKT_LEN, 1, 100, errbuf);
    if (!kmon_handle) fprintf(stderr, "kmon_cap: %s\n", errbuf);
    return kmon_handle ? (char*)"1" : (char*)"0";
}

static char* kmonCapClose(void) {
    if (kmon_handle) { pcap_close(kmon_handle); kmon_handle = NULL; }
    return (char*)"";
}

static char* kmonCapPump(void) {
    if (!kmon_handle) return (char*)"0";
    pcap_dispatch(kmon_handle, 32, kmon_cap_handler, NULL);
    static char buf[16];
    sprintf(buf, "%d", (kmon_qtail - kmon_qhead + KMON_PKT_QUEUE) % KMON_PKT_QUEUE);
    return buf;
}

// Returns next packet as "len:ts_ns:hexdata" or "" if queue empty
static char* kmonCapNext(void) {
    if (kmon_qhead == kmon_qtail) return (char*)"";
    kmon_packet_t* p = &kmon_queue[kmon_qhead];
    kmon_qhead = (kmon_qhead + 1) % KMON_PKT_QUEUE;
    static char out[KMON_MAX_PKT_LEN * 2 + 64];
    int pos = sprintf(out, "%u:%llu:", p->len, (unsigned long long)p->ts_ns);
    for (uint32_t i = 0; i < p->len && pos < (int)sizeof(out) - 3; i++) {
        sprintf(out + pos, "%02x", p->data[i]);
        pos += 2;
    }
    return out;
}

#endif // KMON_CAP_H
