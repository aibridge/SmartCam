#!/usr/bin/env bash

python -u ./enhance/test.py --pretrained_model ./enhance/checkpoints/tenet2-dn-df2k.path --model tenet2 --scale 2 --bias --denoise --sigma 0 \
--test_path ./enhance/input/result.tiff --save_path ./enhance/output --crop_scale 8 --postname df2k --show_info


# if Run out of CUDA memory, just set --crop_scale 4 (or higher)
# remember to change sigma according to the noise level of the current image
# remember to change sigma according to the noise level of the current image