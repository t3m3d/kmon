// protocol.k — JSON message builders for kmon protocol

func protoPacketJson(tsNs, srcIp, dstIp, srcPort, dstPort, protocol, length) {
    let protoName = protocol
    if protocol == "6"  { protoName = "TCP" }
    if protocol == "17" { protoName = "UDP" }
    if protocol == "1"  { protoName = "ICMP" }
    emit "{\"type\":\"packet\",\"data\":{" +
         "\"timestamp\":" + tsNs + "," +
         "\"src_ip\":\"" + srcIp + "\"," +
         "\"dst_ip\":\"" + dstIp + "\"," +
         "\"src_port\":" + srcPort + "," +
         "\"dst_port\":" + dstPort + "," +
         "\"protocol\":\"" + protoName + "\"," +
         "\"length\":" + length + "," +
         "\"info\":\"" + protoName + " " + srcIp + " -> " + dstIp + "\"" +
         "}}\n"
}

func protoStatsJson(mbpsDown, total, tcp, udp, icmp) {
    emit "{\"type\":\"stats\",\"data\":{" +
         "\"mbps_down\":" + mbpsDown + "," +
         "\"mbps_up\":0.000," +
         "\"total_packets\":" + total + "," +
         "\"tcp\":" + tcp + "," +
         "\"udp\":" + udp + "," +
         "\"icmp\":" + icmp + "," +
         "\"vpn_active\":0," +
         "\"vpn_type\":\"\"," +
         "\"vpn_iface\":\"\"" +
         "}}\n"
}

func protoInterfaceJson(iface) {
    emit "{\"type\":\"interface\",\"data\":{\"name\":\"" + iface + "\"}}\n"
}
