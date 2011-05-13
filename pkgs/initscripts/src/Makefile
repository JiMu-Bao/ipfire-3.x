
PROGS = console_check console_init securetty

CC = gcc
CFLAGS += -D_GNU_SOURCE $(shell pkg-config --cflags glib-2.0)

all: $(PROGS)

clean:
	rm -vf $(PROGS) *.o

install:
	-mkdir -pv $(DESTDIR)/lib/udev $(DESTDIR)/sbin
	install -v -m 755 console_check $(DESTDIR)/lib/udev/
	install -v -m 755 console_init $(DESTDIR)/lib/udev/
	install -v -m 755 securetty $(DESTDIR)/sbin

console_check: console_check.o
	$(CC) $(LDFLAGS) -o $@ $<

console_init: console_init.o shvar.o
	$(CC) $(LDFLAGS) $(shell pkg-config --libs glib-2.0) -o $@ $?

securetty: securetty.o
	$(CC) $(LDFLAGS) -o $@ $<
