CC = gcc
CFLAGS = -O3


MYFLAGS = -DDATA_TYPE=double -DMATRIX_WIDTH=100000l -DRATE=16.4 -DCSIZE=0

all: matmatmult.exe matmatmult_zfp.exe

matmatmult.exe:
	g++ -std=c++98 -w -O3 -fPIC -pedantic -mcmodel=large $(MYFLAGS) matmatmult.cpp -o matmatmult.exe

matmatmult_zfp.exe:
	g++ -std=c++98 -w -O3 -fPIC -pedantic -mcmodel=large -I../zfp/include -I../zfp/array -DZFP $(MYFLAGS) matmatmult.cpp -L../zfp/lib -lzfp -o matmatmult_zfp.exe

remake: clean all

clean:
	rm -f matmatmult.exe matmatmult_zfp.exe *.o

