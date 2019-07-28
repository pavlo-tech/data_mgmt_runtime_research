#!/bin/bash

#for i in {0..5000}
#for i in {2001..3000}
#for i in {1001..2000}
for i in {0..1000}
#for i in {0..3000}
do
    echo "Test $i"
   #./SpMV.out aniso/ $i > ./data/multi_$i.txt
   #./SpMV.out aniso/ $i > ./data/dense_single_$i.txt
   #./SpMV.out aniso/ $i > ./data/dense_multi_$i.txt
   #./SpMV.out aniso/ $i > ./data/5dense_multi_$i.txt
   

    ./SpMV.out aniso/ $i > ./data/refactor_$i.txt
   #./SpMV.out aniso/ $i | grep -v "#(0,0)" > ./data/multi_$i.txt
   #./SpMV.out aniso/ $i  > ./data/single_$i.txt
   #./SpMV.out aniso/ $i | grep -v "#(0,0)" > ./data/test_$i.txt
   #./SpMV.out aniso/ $i | grep -v "#(0,0)" > ./data/pwrItr_$i.txt
done  
