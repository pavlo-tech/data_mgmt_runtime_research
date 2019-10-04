


LFLAGS =  -ldl

DIR=$(SDCPROP_PATH)/lib/
LIBS = -L/usr/lib/ -lm  -lstdc++ $(LFLAGS)
CFLAGS = -I.. -w -O3 -fPIC -pedantic


CC = g++ -std=c++98




all: SpMV_ZFP SpMV


MYFLAGS=-DZFP -DRATE=64 -DCSIZE=0
SpMV_ZFP:
	g++ -std=c++98 -I.. -w -O3 -fPIC -pedantic -I../zfp/include -I../zfp/array $(MYFLAGS) -c util.cpp -L../zfp/lib -lzfp
	g++ -std=c++98 -I.. -w -O3 -fPIC -pedantic -I../zfp/include -I../zfp/array $(MYFLAGS) -c init.c -L../zfp/lib -lzfp
	g++ -std=c++98 -I.. -w -O3 -fPIC -pedantic -I../zfp/include -I../zfp/array $(MYFLAGS) -c mmio.c -L../zfp/lib -lzfp
	g++ -std=c++98 -I.. -w -O3 -fPIC -pedantic -I../zfp/include -I../zfp/array $(MYFLAGS) -c main.cpp -L../zfp/lib -lzfp
	g++ -std=c++98 -I.. -w -O3 -fPIC -pedantic -I../zfp/include -I../zfp/array $(MYFLAGS) -o SpMV_zfp.exe mmio.o util.o main.o $(LIBS) -L../zfp/lib -lzfp



SpMV:
	$(CC) $(CFLAGS) -c util.cpp
	#cc -o SpMV.out mmio.o util.o init.o main.o $(LIBS)
	$(CC) $(CFLAGS) -c init.c
	$(CC) $(CFLAGS) -c mmio.c
	$(CC) $(CFLAGS) -c main.cpp
	$(CC) -o SpMV.exe mmio.o util.o main.o $(LIBS)

clean:
	-rm -f SpMV.out
	-rm -f *.o

test:
	./SpMV.out ./aniso/ 

