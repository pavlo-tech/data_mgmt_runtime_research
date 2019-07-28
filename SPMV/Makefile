


LFLAGS =  -ldl

DIR=$(SDCPROP_PATH)/lib/
LIBS = -L/usr/lib/ -lm  -lstdc++ $(LFLAGS)
CFLAGS = -O3 -I.. -c -g -Wall 

MYFLAGS = -DRATE=16.0 -DCSIZE=0

CC = gcc
gpp = g++ -std=c++98 -w -O3 -fPIC -pedantic 



all: SpMV_zfp

SpMV_zfp: mmio_zfp.o util_zfp.o init_zfp.o main_zfp.o
	 g++ -std=c++98 -w -O3 -fPIC -pedantic -I../zfp/include -I../zfp/array $(MYFLAGS) mmio_zfp.o util_zfp.o main_zfp.o -L../zfp/lib -lzfp $(LIBS) -o SpMV_zfp.out

util_zfp.o: util_zfp.c
	$(gpp) $(CFLAGS)  -I../zfp/include -I../zfp/array $(MYFLAGS) util_zfp.c

init_zfp.o: init_zfp.c
	$(gpp) $(CFLAGS) init_zfp.c

mmio_zfp.o: mmio_zfp.c
	$(gpp) $(CFLAGS) mmio_zfp.c

main_zfp.o: main_zfp.c
	$(gpp) $(CFLAGS) main_zfp.c



SpMV: mmio.o util.o init.o main.o
	$(CC) -o SpMV.out mmio.o util.o main.o $(LIBS)
	#cc -o SpMV.out mmio.o util.o init.o main.o $(LIBS)

util.o: util.c
	$(CC) $(CFLAGS) util.c

init.o: init.c
	$(CC) $(CFLAGS) init.c

mmio.o: mmio.c
	$(CC) $(CFLAGS) mmio.c

main.o: main.c
	$(CC) $(CFLAGS) main.c

clean:
	-rm -f SpMV.out
	-rm -f *.o

test:
	./SpMV.out ./aniso/ 

