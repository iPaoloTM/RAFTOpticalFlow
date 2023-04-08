import numpy as np
import argparse
import torch
import matplotlib.pyplot as plt
import torchvision.transforms.functional as F
import cv2
import tempfile
from pathlib import Path
from urllib.request import urlretrieve
from torchvision.io import read_video
from torchvision.models.optical_flow import Raft_Large_Weights
from torchvision.models.optical_flow import raft_large
from torchvision.utils import flow_to_image

#It specifies the portion of the figure to be saved
plt.rcParams["savefig.bbox"] = "tight"

def plot(imgs, args, **imshow_kwargs):
    if not isinstance(imgs[0], list):
        # Make a 2d grid even if there's just 1 row
        imgs = [imgs]

    num_rows = len(imgs)
    num_cols = len(imgs[0])
    _, axs = plt.subplots(nrows=num_rows, ncols=num_cols, squeeze=False)
    for row_idx, row in enumerate(imgs):
        for col_idx, img in enumerate(row):
            ax = axs[row_idx, col_idx]
            img = F.to_pil_image(img.to("cpu"))
            ax.imshow(np.asarray(img), **imshow_kwargs)
            ax.set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])

    plt.tight_layout()
    plt.savefig("flow"+str(args.frame1)+"-"+str(args.frame2)+".png")


def preprocess(img1_batch, img2_batch):

    weights = Raft_Large_Weights.DEFAULT
    transforms = weights.transforms()

    img1_batch = F.resize(img1_batch, size=[520, 960], antialias=False)
    img2_batch = F.resize(img2_batch, size=[520, 960], antialias=False)
    return transforms(img1_batch, img2_batch)

def main(args):
    frames, _, _ = read_video(str("final.mp4"), output_format="TCHW")

    img1_batch = torch.stack([frames[args.frame1], frames[int(args.frame1)+1]])
    img2_batch = torch.stack([frames[args.frame2], frames[int(args.frame2)+1]])

    #plot(img1_batch, "result/",  args)
    #plot(img2_batch, "result/",  args)

    weights = Raft_Large_Weights.DEFAULT
    transforms = weights.transforms()

    img1_batch, img2_batch = preprocess(img1_batch, img2_batch)

    print(f"shape = {img1_batch.shape}, dtype = {img1_batch.dtype}")

    # If you can, run this example on a GPU, it will be a lot faster.
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = raft_large(weights=Raft_Large_Weights.DEFAULT, progress=False).to(device)
    model = model.eval()

    list_of_flows = model(img1_batch.to(device), img2_batch.to(device))
    print(f"type = {type(list_of_flows)}")
    print(f"length = {len(list_of_flows)} = number of iterations of the model")

    predicted_flows = list_of_flows[-1]
    print(f"dtype = {predicted_flows.dtype}")
    print(f"shape = {predicted_flows.shape} = (N, 2, H, W)")
    print(f"min = {predicted_flows.min()}, max = {predicted_flows.max()}")

    flow_imgs = flow_to_image(predicted_flows)

    # The images have been mapped into [-1, 1] but for plotting we want them in [0, 1]
    img1_batch = [(img1 + 1) / 2 for img1 in img1_batch]

    grid = [[img1, flow_img] for (img1, flow_img) in zip(img1_batch, flow_imgs)]
    plot(grid,  args)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--frame1", type=int, required=True, help="First frame")
    parser.add_argument("--frame2", type=int, required=True, help="Second frame")
    args = parser.parse_args()

    main(args)
