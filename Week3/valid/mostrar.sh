
myfiles=`ls ./*.s`

for entry in $myfiles
do
  echo $entry
  printf "\n"
  cat "$entry"
done












