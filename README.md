# RAFT OpticalFlow
Computing optical flow with RAFT architecture (also works with no GPU, just slower)

To start, be sure to create a folder "Results" in your current working directory.
Then, create a folder with the name of your video, in which to save the results of the computed optical flow. In this folder there must be the video named as "final.mp4".

After that, be sure to know how many frames your video is long, then change that value in the file 'runner_optiflow.sh'.

Now we are ready. Just launch './runner_optiflow.sh'
