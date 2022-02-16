import requests
import json
import schedule
import time
import os
import functools
'''
Already installed packages:
pip install python-opencv

pip install requets
pip install schedule
'''

CONFIG_FILE = "config.txt"
ACCESS_TOKEN = "access_token"
PAGE_ID = "page_id"
ALBUM_ID = "album_id"
TOTAL_FRAMES = "total_frames"
POST_EVERY_SEGS = "post_every_segs"
EPISODE_NAME = "episode_name"
SHOW_NAME = "show_name"

class FrameException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self, "Coult not post frame")

def catch_exceptions(cancel_on_failure=False):
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except:
                import traceback
                print(traceback.format_exc())
                if cancel_on_failure:
                    return schedule.CancelJob
        return wrapper
    return catch_exceptions_decorator

#101134099166462 - page id
page_id = '101134099166462'
access_token = 'EAAQn7v6SfBoBAMC4zfoJr4TtPT0wB7cPfeFikXA6hRz7YBIKuuQoyT5129diJ92wEx03hMkbgb1lckKYlZCQGsMLrgHrLgZCbwN7GuqoE9Up9PJS3AntGZCdtrJ2t1iiJ93MLJtEHym4MOhJEy5COaROxnzfOZBvkByIpM45rvvelhLhHPYjptmQQAzsDcDTn6bpn4vG2wZDZD'
album_id = ''
total_frames = 0
post_every_segs = 0
show_name=''
episode_name = ''
frames_posted = 0

def test_facebook_post(test_msg="Test message to facebook group from python"):
    post_url = "https://graph.facebook.com/"+page_id+"/feed"
    payload = {
        'message':test_msg,
        'access_token':access_token
    }
    _request = requests.post(post_url, data=payload)
    return _request

def test_photo_album_post():
    image_url = 'https://graph.facebook.com/105117812101424/photos'#.format(page_id)
    image_location = 'https://frame-bot.s3.amazonaws.com/etrotshfio-framebot/s01e01/Shield+Hero+S01E01+-+frame+2.jpg'
    img_payload = {
    'url': image_location,
    'access_token': access_token,
    'message': "FRAME 02/ABC"
    }
    #Send the POST request
    r = requests.post(image_url, data=img_payload)
    return r

def test_job():
    print("Test job!")

def load_config():
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

@catch_exceptions()
def post_album_frame_facebook():
    print("Frame: "+str(frames_posted))
    facebook_host_api = 'https://graph.facebook.com/{}/photos'.format(album_id)
    #https://frame-bot.s3.amazonaws.com/etrotshfio-framebot/s01e01/Shield+Hero+S01E01+-+frame+2.jpg
    frame_file_name = get_frame_file_name(frames_posted)
    image_location = 'https://frame-bot.s3.amazonaws.com/etrotshfio-framebot/{0}/{1}'.format(episode_name, frame_file_name)
    img_payload = {
    'url': image_location,
    'access_token': access_token,
    'message': "{0} - {1} - Frame: {2} / {3}".format(show_name, episode_name, frames_posted, total_frames)
    }
    #Send the POST request
    response = requests.post(facebook_host_api, data=img_payload)
    response_json = json.loads(response.text)
    print(type(response_json))
    if 'error' in response_json:
        raise FrameException(response_json['error']['message'])
    return response.text

def get_frame_file_name(frame):
    return "Shield-Hero-{0}-f{1}.jpg".format(episode_name,frame)

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
            print(frames_posted)
            condition = frames_posted <= total_frames
        time.sleep(1)
        ellapsed_seconds += 1
    print("All frames posted")

    


if __name__ == '__main__':
    #response1 = test_facebook_post()    
    #print(response1.text)
    #response2 = test_photo_album_post()
    #print(response2.text)
    main()
    '''
    print("START")
    schedule.every(60).seconds.do(test_job)
    for i in range(3):
        schedule.run_pending()
        print("WAITING")
        time.sleep(5)
    print("END")
    schedule.clear()
    '''