CC = gcc
CFLAGS = -O3


#MYFLAGS = -DDATA_TYPE=double -DMATRIX_WIDTH=10l -DRATE=16.4 -DCSIZE=0 -DZFP_WITH_CACHE_FAST_HASH
MYFLAGS = -DDATA_TYPE=double -DMATRIX_WIDTH=10l -DRATE=16.4 -DCSIZE=0 -DZFP_WITH_CACHE_TWOWAY -DZFP_WITH_CACHE_FAST_HASH


test:
	g++ -std=c++98 -w -O3 -fPIC -pedantic -mcmodel=large -I./zfp/include -I./zfp/array -DZFP $(MYFLAGS) test.cpp -L./zfp/lib -lzfp -o test.exe

test2:
	g++ -std=c++98 -w -O3 -fPIC -pedantic -mcmodel=large -I./zfp/include -I./zfp/array -DZFP $(MYFLAGS) matmatmult.cpp -L./zfp/lib -lzfp -o test2.exe

remake_test: clean test test2


clean:
	rm -f test.exe  test2.exe *.o

