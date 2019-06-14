CC = gcc
CFLAGS = -O3

FF = g77
FFLAGS = -O2

MYFLAGS = -DSTREAM_TYPE=double -DSTREAM_ARRAY_SIZE=100000 -DRATE=16.4 -DCSIZE=0
#MYFLAGS = -DSTREAM_TYPE=double -DSTREAM_ARRAY_SIZE=10000000 -DRATE=64.0 -DCSIZE=0

all: stream_c.exe stream_zfp_c.exe

stream_f.exe: stream.f mysecond.o
	$(CC) $(CFLAGS) -c mysecond.c
	$(FF) $(FFLAGS) -c stream.f
	$(FF) $(FFLAGS) stream.o mysecond.o -o stream_f.exe

#$(CC) $(CFLAGS) $(MYFLAGS) stream.c -o stream_c.exe
stream_c.exe: stream.c
	$(CC) $(CFLAGS) $(MYFLAGS) -std=c11 stream.c -o stream_c.exe

#g++ -std=c++98 -O3 -fPIC -Wall -Wextra -pedantic -I../zfp/include -I../zfp/array stream_zfp.cpp -o stream_zfp_c.exe
stream_zfp_c.exe: stream_zfp.cpp
	g++ -std=c++98 -w -O3 -fPIC -pedantic -I../zfp/include -I../zfp/array $(MYFLAGS) stream_zfp.cpp -L../zfp/lib -lzfp -o stream_zfp_c.exe

remake: clean all

clean:
	rm -f stream_f.exe stream_c.exe stream_zfp_c.exe *.o

# an example of a more complex build line for the Intel icc compiler
stream.icc: stream.c
	icc -O3 -xCORE-AVX2 -ffreestanding -qopenmp -DSTREAM_ARRAY_SIZE=80000000 -DNTIMES=20 stream.c -o stream.omp.AVX2.80M.20x.icc
