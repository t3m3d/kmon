// parser.k — raw packet parsing from kmonCapNext() hex format
// Packet format: "len:ts_ns:hexdata"
// Ethernet: 14 bytes, IP starts at offset 14

func pktLen(raw) {
    emit firstpart(raw, ":")
}

func pktTs(raw) {
    let after = afterpart(raw, ":")
    emit firstpart(after, ":")
}

func pktHex(raw) {
    let after = afterpart(raw, ":")
    emit afterpart(after, ":")
}

// Ethernet header is 14 bytes — IP starts at offset 14
// IP header: version/IHL at 14, protocol at 23, src at 26, dst at 30
// TCP/UDP: src port at IP+IHL, dst port at IP+IHL+2

func parsePacket(raw) {
    let hex = pktHex(raw)
    let tsNs = pktTs(raw)
    let length = pktLen(raw)

    if toInt(length) < 34 { emit "" }

    // EtherType at offset 12-13 (big-endian)
    let etherType = kmonCapU16(hex, "12")
    if etherType != "2048" { emit "" }  // 0x0800 = IPv4 only

    // IP protocol at offset 23
    let protocol = kmonCapByte(hex, "23")

    // IP IHL (header length) = lower nibble of byte 14, in 32-bit words
    let ihlByte = toInt(kmonCapByte(hex, "14"))
    let ihl = (ihlByte % 16) * 4

    // Source IP at offset 26 (4 bytes, big-endian)
    let srcIpRaw = kmonCapU32(hex, "26")
    let dstIpRaw = kmonCapU32(hex, "30")
    let srcIp = ipToStr(srcIpRaw)
    let dstIp = ipToStr(dstIpRaw)

    // TCP/UDP ports at IP payload start (14 + ihl)
    let payloadOff = 14 + ihl
    let srcPort = "0"
    let dstPort = "0"
    if protocol == "6" || protocol == "17" {
        srcPort = kmonCapU16(hex, payloadOff + "")
        dstPort = kmonCapU16(hex, payloadOff + 2 + "")
    }

    emit tsNs + "|" + srcIp + "|" + dstIp + "|" + srcPort + "|" + dstPort + "|" + protocol + "|" + length
}
