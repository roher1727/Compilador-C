myfiles=`ls ./*.c`

for entry in $myfiles
do
  echo $entry
  printf "\n"
  cat "$entry"
done
