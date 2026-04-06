// protocol.k — JSON message builders for kmon protocol

func protoPacketJson(tsNs, srcIp, dstIp, srcPort, dstPort, protocol, length) {
    emit "{\"type\":\"packet\",\"data\":{" +
         "\"timestamp\":" + tsNs + "," +
         "\"src_ip\":\"" + srcIp + "\"," +
         "\"dst_ip\":\"" + dstIp + "\"," +
         "\"src_port\":" + srcPort + "," +
         "\"dst_port\":" + dstPort + "," +
         "\"protocol\":" + protocol + "," +
         "\"length\":" + length +
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
