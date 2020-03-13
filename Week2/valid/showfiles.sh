myfiles=`ls ./*.c`

for entry in $myfiles
do
  gcc -S -O3 -fno-asynchronous-unwind-tables "$entry"
done
