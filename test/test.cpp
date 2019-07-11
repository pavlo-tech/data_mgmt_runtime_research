#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctime>
#include <math.h>

#include "zfparray2.h"




int main()
{
		printf("rate,matrix_wdith,cache_size\n");
for(int r = 1; r < 64; r*=2)
{
	zfp::array2<DATA_TYPE> 
		A_32(32, 32, r, 0, 0),
		A_128(128, 128, r, 0, 0),
		A_256(256, 256, r, 0, 0),		
		A_384(384, 384, r, 0, 0),
		A_512(512, 512, r, 0, 0),
		A_576(576, 576, r, 0, 0),
		A_768(768, 768, r, 0, 0),
		A_1024(1024, 1024, r, 0, 0),
		A_1536(1536, 1536, r, 0, 0),
		A_2048(2048, 2048, r, 0, 0),
		A_4096(4096, 4096, r, 0, 0);


		printf("%d,%d,%d\n",r,32,A_32.cache_size());
		printf("%d,%d,%d\n",r,128,A_128.cache_size());
		printf("%d,%d,%d\n",r,256,A_256.cache_size());
		printf("%d,%d,%d\n",r,384,A_384.cache_size());
		printf("%d,%d,%d\n",r,512,A_512.cache_size());
		printf("%d,%d,%d\n",r,576,A_576.cache_size());
		printf("%d,%d,%d\n",r,768,A_768.cache_size());
		printf("%d,%d,%d\n",r,1024,A_1024.cache_size());
		printf("%d,%d,%d\n",r,1536,A_1536.cache_size());
		printf("%d,%d,%d\n",r,2048,A_2048.cache_size());
		printf("%d,%d,%d\n",r,4096,A_4096.cache_size());
/*
delete A_32; 
delete A_128;
delete A_256;
delete A_384;
delete A_512;
delete A_576;
delete A_768;
delete A_1024;
delete A_1536;
delete A_2048;*/
}
}



