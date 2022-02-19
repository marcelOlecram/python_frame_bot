"""
The code on this file is based on this tutorial: https://www.thepythoncode.com/article/extract-frames-from-videos-in-python
I made some adjustments to suit my needs
"""
from datetime import timedelta
import cv2
from cv2 import IMWRITE_JPEG2000_COMPRESSION_X1000
import numpy as np
import os
import time

def format_timedelta(time_delta):
    """
    Utility function to format timedelta (e.g 00:00:20.05) 
    omitting microseconds and retaining milliseconds
    """
    result = str(time_delta)
    try:
        result, ms = result.split(".")
    except ValueError:
        return result + ".00"#.replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}"#.replace(":", "-")

def get_frames(cap, saving_fps):
    """
    Extract de frames timings of the video capture
    ----
    cap : VideoCapture
        VideoCapture obtained from cv2
    saving_fps: int
        Frames per second. The amount of frames per second desired to extract.
    """
    s = []
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Number of 'real' frames: {frame_count}")
    print(f"Video fps: {video_fps}")
    clip_duration = frame_count / video_fps
    print(f"Video duration: {clip_duration } seg")
    frame_interval = 1 / saving_fps
    print(f"Extracting a frame every: {frame_interval} seg")
    for i in np.arange(0, clip_duration, frame_interval):
        s.append(i)
    return s

def main(video_file, frames_per_second=6):
    start_time = time.time()
    print(f"Extracting frames of video file: {video_file}");
    print(f"Frames per second: {frames_per_second}");
    filename, _ = os.path.splitext(video_file)
    file_raw_name, _ = os.path.splitext(os.path.basename(video_file))
    filename += "- frames"
    if not os.path.isdir(filename):
        print(f"Creating directory: {filename}")
        os.mkdir(filename)
    else:
        print(f"Directory: {filename} already exists")
    
    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    saving_frames_per_second = min(fps, frames_per_second)
    saving_frames_durations = get_frames(cap, saving_frames_per_second)
    calculated_frames = len(saving_frames_durations)
    print("Number of frames calculated: " + str(calculated_frames))
    count,extracted_frame_count = 0,0
    while True:
        is_read, frame = cap.read()
        if not is_read:
            # break out of the loop if there are no frames to read
            break
        # get the duration by dividing the frame count by the FPS
        frame_duration = count / fps
        try:
            # get the earliest duration to save
            closest_duration = saving_frames_durations[0]
        except IndexError:
            # the list is empty, all duration frames were saved
            break
        if frame_duration >= closest_duration:
            extracted_frame_count += 1
            # if closest duration is less than or equals the frame duration, 
            # then save the frame
            frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
            print(f"Extracted frame {extracted_frame_count} / {calculated_frames} at time: {frame_duration_formatted}")
            #print(type(frame))
            frame_count_str = str(extracted_frame_count)
            final_file =os.path.join(filename, f"{file_raw_name}-f{frame_count_str.zfill(5)}.jpg") 
            #cv2.imwrite(final_file, frame, [int(IMWRITE_JPEG2000_COMPRESSION_X1000),0]) # image compression.
            cv2.imwrite(final_file, frame) 
            # drop the duration spot from the list, since this duration spot is already saved
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        # increment the frame count
        count += 1
    stop_time = time.time()
    ellapsed_time_ms = (stop_time - start_time) * 1000
    print(f"Frames extracted! - ellapsed time: {ellapsed_time_ms} ms")

if __name__ == '__main__':
    import sys
    video_file = sys.argv[1]
    if(not os.path.isfile(video_file)):
        print("No file found")

    arguments = len(sys.argv)
    if(arguments==2):
        main(video_file)
    elif(arguments==3):
        frames_per_second = float(sys.argv[2])
        main(video_file, frames_per_second)
    else:
        print("too many arguments")

