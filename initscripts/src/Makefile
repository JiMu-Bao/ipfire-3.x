
PROGS = ipcalc securetty

CC = gcc
CFLAGS += -D_GNU_SOURCE $(shell pkg-config --cflags glib-2.0)

all: $(PROGS)

clean:
	rm -vf $(PROGS) *.o

test: ipcalc
	./ipcalc-tests

install: $(PROGS)
	# Install binaries
	-mkdir -pv $(DESTDIR)/lib/udev $(DESTDIR)/{,s}bin
	install -v -m 755 ipcalc $(DESTDIR)/bin
	install -v -m 755 securetty $(DESTDIR)/sbin

	# Install man pages
	-mkdir -pv $(DESTDIR)/usr/share/man/man1
	-mkdir -pv $(DESTDIR)/usr/share/man/man8
	install -v -m 644 ipcalc.1 $(DESTDIR)/usr/share/man/man1
	install -v -m 644 securetty.8 $(DESTDIR)/usr/share/man/man8

ipcalc: ipcalc.o
	$(CC) $(LDFLAGS) -o $@ $< -lpopt

securetty: securetty.o
	$(CC) $(LDFLAGS) -o $@ $<
