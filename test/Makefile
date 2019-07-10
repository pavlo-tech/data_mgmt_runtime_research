CC = gcc
CFLAGS = -O3


MYFLAGS = -DDATA_TYPE=double -DMATRIX_WIDTH=10l -DRATE=16.4 -DCSIZE=0


test:
	g++ -std=c++98 -w -O3 -fPIC -pedantic -mcmodel=large -I../zfp/include -I../zfp/array -DZFP $(MYFLAGS) test.cpp -L../zfp/lib -lzfp -o test.exe

remake_test: clean test


clean:
	rm -f test.exe *.o

