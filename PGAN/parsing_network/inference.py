"""Run DeepLab-ResNet on a given image.

This script computes a segmentation mask for a given image.
"""

from __future__ import print_function

import argparse
from datetime import datetime
import os
import sys
import time

from PIL import Image

import tensorflow as tf
import numpy as np

from deeplab_resnet import DeepLabResNetModel, ImageReader, decode_labels, prepare_label

import pdb

from utils.filters import *

IMG_MEAN = np.array((104.00698793,116.66876762,122.67891434), dtype=np.float32)
    
CURRENT_DIR = os.getcwd()
NUM_CLASSES = 7
DATA_LIST = r'.\dataset\dance.txt'
SAVE_DIR = r'.\output'
#MODEL_WEIGHTS = os.path.join(CURRENT_DIR,'models', 'checkpoint','final_model')
MODEL_WEIGHTS= r'.\models\final_model\model.ckpt-19315'
IMAGE_PATH=r'.\input'
def get_arguments():
    """Parse all the arguments provided from the CLI.
    
    Returns:
      A list of parsed arguments.
    """
    parser = argparse.ArgumentParser(description="DeepLabLFOV Network Inference.")
    parser.add_argument("--img_path", type=str,
                        help="Path to the RGB image file folder.", default=IMAGE_PATH)
    parser.add_argument("--model_weights", type=str,
                        help="Path to the file with model weights.", default=MODEL_WEIGHTS)
    parser.add_argument("--data_list", type=str, default=DATA_LIST,
                        help="Path to the image list.")
    parser.add_argument("--num-classes", type=int, default=NUM_CLASSES,
                        help="Number of classes to predict (including background).")
    parser.add_argument("--save-dir", type=str, default=SAVE_DIR,
                        help="Where to save predicted mask.")
    return parser.parse_args()

def load(saver, sess, ckpt_path):
    '''Load trained weights.
    
    Args:
      saver: TensorFlow saver object.
      sess: TensorFlow session.
      ckpt_path: path to checkpoint file with parameters.
    ''' 
    saver.restore(sess, ckpt_path)
    print("Restored model parameters from {}".format(ckpt_path))

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def main():
    """Create the model and start the evaluation process."""
    args = get_arguments()
    #num_steps = file_len(args.data_list)
    num_steps=1
    # Create queue coordinator.
    coord = tf.train.Coordinator()
    
    # Load reader.
    frame = Image.open('./input/1.jpg')
    image_batch = tf.placeholder(tf.float32, shape=[None,frame.size[1],frame.size[0],3]) # Add one batch dimension.
    
    # Create network.
    net = DeepLabResNetModel({'data': image_batch}, is_training=False, num_classes=args.num_classes)

    # Which variables to load.
    restore_var = tf.global_variables()

    # Predictions.
    raw_output = net.layers['fc1_voc12']
    raw_output_up = tf.image.resize_bilinear(raw_output, tf.shape(image_batch)[1:3,])
    raw_output_up = tf.argmax(raw_output_up, dimension=3)
    pred = tf.expand_dims(raw_output_up, dim=3)

    
    # Set up TF session and initialize variables. 
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)
    init = tf.global_variables_initializer()
    
    sess.run(init)
    
    # Load weights.
    loader = tf.train.Saver(var_list=restore_var)
    load(loader, sess, args.model_weights)
    
    # Start queue threads.
    threads = tf.train.start_queue_runners(coord=coord, sess=sess)

    start_time = time.time()
    if not os.path.exists(args.save_dir):
      os.makedirs(args.save_dir)
    # Perform inference.
    for step in range(num_steps):
        frame = Image.open('./input/1.jpg')
        preds,  = sess.run([pred], feed_dict={image_batch:np.expand_dims(np.asarray(frame),0).astype(np.float32) })
        jpg_path=r'.\input\1.jpg'
        preds[preds!=2]=0
        msk = decode_labels(preds, num_classes=args.num_classes)
        with open('preds.txt','wb') as file:
            file.write(preds)
        im = Image.fromarray(msk[0])
        im2=np.array(im)
        x,y,_ = np.nonzero(im2)
        print(np.mean(x), np.mean(y))
        img_o = Image.open(jpg_path)
        jpg_path = jpg_path.split('\\')[-1].split('.')[0]
        img = np.array(im)*0.9 + np.array(img_o)*0.7
        print(img.shape)
        x ,y=np.mean(x).astype(np.int), np.mean(y).astype(np.int)
        img_o=np.array(img_o)
        img =Liquify(img_o,x,y)
        img[img>255] = 255
        img = Image.fromarray(np.uint8(img))
        img.save(args.save_dir + '\\'+jpg_path + '.png')
        print('Image processed {}.png'.format(jpg_path))
    
    total_time = time.time() - start_time
    print('The output files have been saved to {}'.format(args.save_dir))
    print('It took {} sec on each image.'.format(total_time/num_steps))
    
if __name__ == '__main__':
    main()
