// server.k — TCP server for Python frontend (port 9090)

import "winsock.krh"

let srvClient = "0"

func serverStart() {
    let wsa = structNew("WSADATA")
    WSAStartup("514", wsa)

    let s = socket("2", "1", "6")

    let addr = structNew("SOCKADDR_IN")
    structSet(addr, "sin_family", "2")
    structSet(addr, "sin_port", htons("9090") + "")
    structSet(addr, "sin_addr", inet_addr("127.0.0.1") + "")

    bind(s, addr, "16")
    listen(s, "1")

    printErr("kmon: waiting for frontend on port 9090...")
    srvClient = accept(s, "0", "0") + ""
    printErr("kmon: frontend connected.")
    emit ""
}

func serverSend(msg) {
    if srvClient == "0" || srvClient == "-1" { emit "" }
    send(srvClient, msg, len(msg) + "", "0")
    emit ""
}

func serverStop() {
    if srvClient != "0" && srvClient != "-1" {
        shutdown(srvClient, "2")
        closesocket(srvClient)
    }
    WSACleanup()
    emit ""
}
