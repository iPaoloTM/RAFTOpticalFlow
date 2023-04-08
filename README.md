# RAFT OpticalFlow
Computing optical flow with RAFT architecture (also works with no GPU, just slower)

To start, be sure to create a folder __results__ in your current working directory.
Then, create a folder with the name of your video, in which to save the results of the computed optical flow. In this folder there must be the video named as __final.mp4__.

It should look like this
`current_directory
├── results/
│   └─── video_name/
│         └─── final.mp4
├── runner_optiflow.sh
└── optiflow.py
`

After that, be sure to know how many frames your video is long, then change that value in the file `runner_optiflow.sh`.
Also, change the --input tag in the file `runner_optiflow.sh` with the name of the video you will work on.

Now we are ready. Just launch `./runner_optiflow.sh`

After having computed the optical flow for each couple of successive frames, be sure to change in `rename.sh` the correct number of frames to be renamed,  launch `rename.sh`.

Now execute `ffmpeg -f image2 -framerate 30 -i flow%d.png -loop -1 flow.gif` to finally generate the GIF visualazing the optical flow.


This code is based on the original paper of RAFT: https://arxiv.org/abs/2003.12039
