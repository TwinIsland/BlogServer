# Variables
ZIG = zig
TARGET = main
LIBS = -lc -lsqlite3
SRC = main.zig
OUT = $(TARGET)

# Default target
all: $(OUT)

$(OUT): $(SRC) sqlite3.zig
	$(ZIG) build-exe $(SRC) $(LIBS) -o $(OUT)

clean:
	rm -f $(OUT)
