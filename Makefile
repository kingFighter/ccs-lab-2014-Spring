ASFLAGS := -m32
CFLAGS  := -m32 -g -std=c99 -Wall -Werror -D_GNU_SOURCE
LDFLAGS := -m32
LDLIBS  := -lcrypto
PROGS   := zookld zookfs zookd

all: $(PROGS)
.PHONY: all

zookld zookd zookfs: %: %.o http.o


.PHONY: check
check: $(PROGS)
	./check-lab5.sh



.PHONY: clean
clean:
	rm -f *.o *.pyc *.bin $(PROGS)


lab%-handin.tar.gz: clean
	tar cf - `find . -type f | grep -v '^\.*$$' | grep -v '/CVS/' | grep -v '/\.svn/' | grep -v '/\.git/' | grep -v 'lab[0-9].*\.tar\.gz' | grep -v '/submit.token$$'` | gzip > $@

.PHONY: prepare-submit
prepare-submit: lab5-handin.tar.gz

.PHONY: submit
submit: lab5-handin.tar.gz
	./submit.py $<

.PRECIOUS: lab5-handin.tar.gz
