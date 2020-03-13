myfiles=`ls ./*.s`

for entry in $myfiles
do
  printf "\n"
  cat "$entry"
done
