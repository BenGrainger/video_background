import pims
import numpy as np
import subprocess
import os
import time
import math
import matplotlib.pyplot as plt
import cv2

def cut_video(input_vid_dir, input_vid_name, start_seconds, end_seconds, clip_number, clip_path, last_or_no):
    """
    this method is super fast as it does not rely on encoding and deconding the video into wrappers and uses straight ffmpeg
    """
    
    # create name of video to be outputted
    output_name = input_vid_name[:-4] + 'short_{}.avi'.format("{:02d}".format(clip_number+1))
    output_path = os.path.join(clip_path, output_name)
    
    # create name of video to be outputted
    input_vid_path = os.path.join(input_vid_dir, input_vid_name)
    
    # format seconds into hh:mm:float(ss)
    start_seconds = time.strftime('%H:%M:%S', time.gmtime(start_seconds))
    end_seconds = time.strftime('%H:%M:%S', time.gmtime(end_seconds))
    
    # command format: 'ffmpeg -ss first_clip -i input_video_string -c copy -t second_clip output_video_string'
    
    if last_or_no == False:
        command = 'ffmpeg -ss {} -i {} -c copy -t {} {}'.format(start_seconds, input_vid_path, end_seconds, output_path)
        print(command)
    else:
        command = 'ffmpeg -ss {} -i {} -c copy {}'.format(start_seconds, input_vid_path, output_path)
        print(command)
    # this copies and clips the video. first number clips the first seconds, then clip everything that is seconds after that
    
    result = subprocess.run(command)
    
    
    
def get_length(filename):
    """
    returns length of the video in seconds as a float
    """
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)



def create_sliced_video(directory, video_for_slicing, division_number):
    """
    takes in video, spits out a folder containing shorter clips
    """
    video = os.path.join(directory, video_for_slicing)
    
    # create directoy for short clips
    clip_path = os.path.join(directory, video_for_slicing[:-4] + '_clips')
    os.mkdir(clip_path)
    
    # get length of video and length of clips based on the number of clips we want
    length = get_length(video)
    clip_length = length/division_number
    clip_length = math.floor(clip_length)
    
    # enumerate through clip numbers writing each one to the short clip directory
    for clip_number in range(division_number):
        
        start_seconds = clip_length*clip_number
        
        if clip_number == division_number-1:
            cut_video(directory, video_for_slicing, start_seconds, clip_length, clip_number, clip_path, True)
            
        else:
            cut_video(directory, video_for_slicing, start_seconds, clip_length, clip_number, clip_path, False)
            

folder = r'C:\Users\BMLab21\Documents\CrabStreams'
contents = os.listdir(folder)
for file_name in contents:
    if '.avi' in file_name:
        output_name = file_name[:-4] + suffix
        if len(output_name) == len('YYYY-MM-DD_265.avi'):
            create_sliced_video(folder, output_name, 12)