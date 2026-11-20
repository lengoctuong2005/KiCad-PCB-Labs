CC ?= gcc
CFLAGS ?= -Wall -Wextra -Werror -pedantic -std=c99 -Imain

all: test

test: tests/test_runner
	./tests/test_runner
	python3 tests/check_acquisition_regression.py

tests/test_runner: tests/test_ptt_firmware_logic.c main/esp32_ptt_streamer.h
	$(CC) $(CFLAGS) tests/test_ptt_firmware_logic.c -o $@

clean:
	rm -f tests/test_runner

.PHONY: all test clean
