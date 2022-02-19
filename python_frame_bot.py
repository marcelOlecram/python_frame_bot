import requests
import json
import schedule
import time
import os
import functools
from frame_exceptions import FrameException

# Constants to get configuration data
CONFIG_FILE = "config.txt"
ACCESS_TOKEN = "access_token"
PAGE_ID = "page_id"
ALBUM_ID = "album_id"
TOTAL_FRAMES = "total_frames"
POST_EVERY_SEGS = "post_every_segs"
EPISODE_NAME = "episode_name"
SHOW_NAME = "show_name"

# Global variables. Will be loaded from config.txt
page_id = ''
access_token = ''
album_id = ''
total_frames = 0
post_every_segs = 0
show_name=''
episode_name = ''
frames_posted = 0

#Handling exceptions (based on schedule module docs)
def catch_exceptions(cancel_on_failure=False):
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except FrameException as fe:
                post_facebook_message(fe.get_message)
                print(fe.message)
                if cancel_on_failure:
                    return schedule.CancelJob            
            except:
                import traceback
                post_facebook_message(traceback.format_exc())
                print(traceback.format_exc())
                if cancel_on_failure:
                    return schedule.CancelJob            

        return wrapper
    return catch_exceptions_decorator

def load_config():
    """
    Loads the configuration data from config.txt
    """
    print("Loading configs")
    if(not os.path.isfile(CONFIG_FILE)):
        print("No config file found")
        return False        
    file_config = open("config.txt","r")
    for file_line in file_config:
        if ACCESS_TOKEN in file_line :
            global access_token
            access_token = file_line.split(':')[1].strip()
            print("access_token found")
            continue
        if PAGE_ID in file_line:
            global page_id
            page_id = file_line.split(':')[1].strip()
            print("page_id found")
            continue
        if ALBUM_ID in file_line:
            global album_id
            album_id = file_line.split(':')[1].strip()
            print("album_id found")
            continue
        if TOTAL_FRAMES in file_line:
            global total_frames
            total_frames = int(file_line.split(':')[1].strip())
            print("total_frames found")
            continue
        if POST_EVERY_SEGS in file_line:
            global post_every_segs
            post_every_segs = int(file_line.split(':')[1].strip())
            print("post_every_segs found")
            continue    
        if EPISODE_NAME in file_line:
            global episode_name
            episode_name = file_line.split(':')[1].strip()
            print("episode_name found")
            continue    
        if SHOW_NAME in file_line:
            global show_name
            show_name = file_line.split(':')[1].strip()
            print("show_name found")
            continue    
    return True

def post_facebook_message(message:str):
    """
    Post a single text to page

    Parameters
    --------
    message: str
        Text to post
    """
    post_url = f"https://graph.facebook.com/{page_id}/feed"
    payload = {
        'message':message,
        'access_token':access_token
    }
    _request = requests.post(post_url, data=payload)
    return _request

@catch_exceptions()
def post_album_frame_facebook():
    """
    Post image to facebook.

    Post the image stored, the url of the image is calculated
    """
    print(f"Frame: {frames_posted} of {total_frames}")
    facebook_host_api = 'https://graph.facebook.com/{}/photos'.format(album_id)
    frame_file_name = get_frame_file_name(frames_posted)
    image_location = 'https://frame-bot.s3.amazonaws.com/etrotshfio-framebot/{0}/{1}'.format(episode_name, frame_file_name)
    img_payload = {
    'url': image_location,
    'access_token': access_token,
    'message': "{0} - {1} - Frame: {2} / {3}".format(show_name, episode_name, frames_posted, total_frames)
    }
    response = requests.post(facebook_host_api, data=img_payload)
    response_json = json.loads(response.text)
    if 'error' in response_json:
        raise FrameException(response_json['error']['message'], frames_posted)
    return response.text

def get_frame_file_name(frame):
    """
    Builds the frame image file name
    """
    frame_zfill = (str(frame)).zfill(5)
    return "Shield-Hero-{0}-f{1}.jpg".format(episode_name,frame_zfill)

def main():
    print("Frame bot started.")
    if not load_config():
        print("No config file found")
        return

    global frames_posted
    schedule.every(post_every_segs).seconds.do(post_album_frame_facebook)
    condition = frames_posted < total_frames
    print("Started posting frames")
    ellapsed_seconds = 0
    while condition:
        schedule.run_pending()
        if ellapsed_seconds % post_every_segs == 0:
            frames_posted += 1
            condition = frames_posted <= total_frames
        time.sleep(1)
        ellapsed_seconds += 1
    print("All frames posted")

if __name__ == '__main__':
    main()    