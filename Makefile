# Compiler and flags
CC = gcc
CFLAGS = -O2 -Wall -Iinclude -I/c/npcap-sdk/Include

# Linker flags (Npcap + Winsock)
LDFLAGS = -L/c/npcap-sdk/Lib/x64 -lwpcap -lws2_32


# Source files
BACKEND_SRC = backend/cap.c backend/par.c backend/stats.c backend/util.c
API_SRC = api/protocol.c api/server.c
MAIN_SRC = backend/main.c

SRC = $(BACKEND_SRC) $(API_SRC) $(MAIN_SRC)

# Output binary
OUT = kmon_backend.exe

# Default target
all: $(OUT)

$(OUT): $(SRC)
	$(CC) $(CFLAGS) -o $(OUT) $(SRC) $(LDFLAGS)

# Clean build artifacts
clean:
	rm -f $(OUT) *.o backend/*.o api/*.o