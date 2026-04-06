import "kmon_cap.krh"
import "windows.krh"
import "winsock.krh"

import "kmon_utils.k"
import "util.k"
import "stats.k"
import "parser.k"
import "protocol.k"
import "server.k"

just run {
    let iface = arg("0")
    if iface == "" {
        printErr("Usage: kmon <network-interface>")
        emit 1
    }

    printErr("kmon backend starting...")

    // Open capture
    let ok = kmonCapOpen(iface)
    if ok == "0" {
        printErr("kmon: failed to open interface: " + iface)
        emit 1
    }
    printErr("kmon: capturing on " + iface)

    // Start TCP server — blocks until Python connects
    serverStart()

    // Init stats
    let ts = timestampNs()
    statsInit(ts)

    let lastStats = ts
    let running = "1"

    while running == "1" {
        // Pump packets from pcap into queue
        kmonCapPump()

        // Process all queued packets
        let raw = kmonCapNext()
        while raw != "" {
            let parsed = parsePacket(raw)
            if parsed != "" {
                let tsNs    = firstpart(parsed, "|")
                let rest    = afterpart(parsed, "|")
                let srcIp   = firstpart(rest, "|")
                rest        = afterpart(rest, "|")
                let dstIp   = firstpart(rest, "|")
                rest        = afterpart(rest, "|")
                let srcPort = firstpart(rest, "|")
                rest        = afterpart(rest, "|")
                let dstPort = firstpart(rest, "|")
                rest        = afterpart(rest, "|")
                let proto   = firstpart(rest, "|")
                let pktLen2 = afterpart(rest, "|")

                statsUpdate(proto, pktLen2)

                let json = protoPacketJson(tsNs, srcIp, dstIp, srcPort, dstPort, proto, pktLen2)
                serverSend(json)
            }
            raw = kmonCapNext()
        }

        // Send stats every second
        let now = timestampNs()
        if toInt(now) - toInt(lastStats) >= 1000000000 {
            let snap    = statsSnapshot(now)
            let mbps    = firstpart(snap, ",")
            let rest2   = afterpart(snap, ",")
            let total   = firstpart(rest2, ",")
            rest2       = afterpart(rest2, ",")
            let tcpC    = firstpart(rest2, ",")
            rest2       = afterpart(rest2, ",")
            let udpC    = firstpart(rest2, ",")
            let icmpC   = afterpart(rest2, ",")
            let sjson   = protoStatsJson(mbps, total, tcpC, udpC, icmpC)
            serverSend(sjson)
            lastStats = now
        }
    }

    serverStop()
    kmonCapClose()
    emit 0
}
