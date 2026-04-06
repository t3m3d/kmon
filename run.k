// kmon_main.k — main entry point for kmon with HTTP UI
// Serves kmon_ui.html on :8080, streams packets+stats via SSE
// Usage: kmon.exe <interface>

import "kmon_cap.krh"
import "kmon_http.krh"
import "windows.krh"

import "kmon_utils.k"
import "util.k"
import "stats.k"
import "parser.k"
import "protocol.k"

just run {
    let iface = arg("0")
    if iface == "" {
        printErr("Usage: kmon <network-interface>")
        emit 1
    }

    // Init HTTP server + load UI
    let htmlOk = kmonHttpInit("kmon_ui.html")
    if htmlOk == "0" {
        printErr("kmon: failed to load kmon_ui.html")
        emit 1
    }

    // Open packet capture
    let capOk = kmonCapOpen(iface)
    if capOk == "0" {
        printErr("kmon: failed to open interface: " + iface)
        emit 1
    }
    printErr("kmon: capturing on " + iface)

    // Open browser
    kmonHttpOpenBrowser()

    // Init stats state
    let ts        = timestampNs()
    let statsState = statsInit(ts)
    let lastStats  = ts

    // Interface JSON
    let ifaceJson = protoInterfaceJson(iface)

    let running = "1"
    while running == "1" {
        // Accept new HTTP connections
        kmonHttpPoll()

        // Broadcast interface info
        kmonHttpBroadcast(trim(ifaceJson))

        // Pump packets from pcap queue
        kmonCapPump()
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

                statsState = statsUpdate(statsState, proto, pktLen2)

                let json = protoPacketJson(tsNs, srcIp, dstIp, srcPort, dstPort, proto, pktLen2)
                kmonHttpBroadcast(trim(json))
            }
            raw = kmonCapNext()
        }

        // Send stats every second
        let now = timestampNs()
        if toInt(now) - toInt(lastStats) >= 1000000000 {
            let snapshotResult = statsSnapshot(statsState, now)
            statsState = firstpart(snapshotResult, "|")
            let snap   = afterpart(snapshotResult, "|")
            let mbps   = firstpart(snap, ",")
            let rest2  = afterpart(snap, ",")
            let total  = firstpart(rest2, ",")
            rest2      = afterpart(rest2, ",")
            let tcpC   = firstpart(rest2, ",")
            rest2      = afterpart(rest2, ",")
            let udpC   = firstpart(rest2, ",")
            let icmpC  = afterpart(rest2, ",")
            let sjson  = protoStatsJson(mbps, total, tcpC, udpC, icmpC)
            kmonHttpBroadcast(trim(sjson))
            lastStats = now
        }
    }

    kmonCapClose()
    kmonHttpStop()
    emit 0
}
