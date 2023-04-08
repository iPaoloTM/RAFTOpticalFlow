#change the upper limit of the sequence with the actual number of frames of the video
for i in $(seq 0 47)
do
    mv flow${i}-$((i+1)).png flow${i}.png 
done
