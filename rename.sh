for i in $(seq 0 47)
do
    mv flow${i}.png flow${i}-$((i+1)).png 
done
