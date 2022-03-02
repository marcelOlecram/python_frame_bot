# Python Frame Bot

An open source frame bot. This project is my own personal take on a frame bot. I found other similar projects not able to suit my needs. 

Only considers posting frames to facebook via graph api.

The project also contains the script to extract the frames of a video.

Developed under Python 3.10.2

## Frame-bot?

Basically a python script which will post to social media every certain amount of time. That's it.

## Running

### Video extractor

To extract frames of a video run this script separatedly.

> `python video_frame_extractor.py` *path/to/file.mp4 [frames per second]*

You can specify the amount of frames per second you want to extract, if not specified the default value is 6 frames per second.
### Frame posting
First you should have the frames extracted and host them. You also should set organized structure to access the files URL easily.

Before running the script, you should create a `config.txt` in the same folder as the script.
The file is not included in the project for obvious reasons.

This file has all the variables that will be loaded to post the frames. The properties should be one per line separated by `:`

|Config Property|Description|
|-|-|
|access_token|your facebook (meta) api access token|
|page_id|Your facebook page id. Not necessairly used right now|
|album_id|Your album id where to post the frames|
|frame_host|URL base where you host the frames (s3 for example)|
|start_frame|From which frame to start posting|
|total_frames|How many frames are gonna to be posted|
|post_every_segs|The amount of time (segs) in between frame posts to make|
|episode_name|The name of the file. Used for both post message and building the specific URL to the frame|
|show_name|The name of the video or show. Used for post message|

The file must have
Run the python script:

>```python python_frame_bot.py```

No additional arguments are required.

#### Functioning

The script schedules the posting of frames between the seconds specified (`post_every_segs`). It will start at the specified frame (`start_frame`) to all the frames (`total_frames`). Every post will include a message specifyng the show or video name (`show_name`), episode (`episode_name`), and current frame.

When posting a frame, the script will dinamically build the URL ( based on `frame_host`) to the frame based on the current frame, show or video and episode