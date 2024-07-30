# YouTube Timestamps Extractor
## Overview
This python package is used to generate a dataset that is to be used to finetune a large language model to extract timestamps from youtube video descriptions.
Youtube Timsestamps indicate the start and end times of different sections of a video and can be used to navigate to differenr sections of a video.
## Example
For example in the video [Removing Stars From a String - Leetcode 2390 - Python](https://www.youtube.com/watch?v=pRyFZIaKegA&list=PLQpVsaqBj4RLwXMZ9LaAFf4rVowiC3ZcG&index=1) by neetcodeio:
```
0:00 - Read the problem
0:30 - Drawing Explanation
2:45 - Coding Explanation
```
```i.e start time : end time - Title```
They enable the viwer to jump to the video section that interests them. From a developers pesperctive, they can be used to split a video into different sections for transcription and summarization. There are two ways to get the timestamps from the video description:
1. Using regex
2. Using a large language model
## The motivation
Getting the video timestamps is especially useful when you need to transcribe a video since models like openai whisper require a certain lenght of audio as input. The timestamps enable the transcription and further analysis of video sections that deal with particular topics.
## Why Large language models?
Coming up with a regex for extracting the time stamp is quite challenging and does not generalize well. You have to come up with ways to handle numerous edge cases, requiring very complex patterns. In this case a sample regex may be:
- Match one or more digits i.e ``0``
- Then match a space foolowed by a colon followed by anaother space i.e `` : ``
- Then match one or more digits i.e ``00``
- Them match a space, followed by a dash then another space i.e `` - ``
- Then match an unknown number of charatcters followed by a new line i.e ``Read the problem``
- Then repeat this an unknown number of times

The dataset created created will be used to finetune an llm that when given a video description, will extract the timestamps and return a json object that contains the time stamps i.e
```python
{'video_id': '6st4IxEF-90',
 'time_stamps': [{'start_time': '0:00',
   'end_time': '0:50',
   'title': 'Read the problem'},
  {'start_time': '0:50', 'end_time': '10:10', 'title': 'Drawing Explanation'},
  {'start_time': '10:10', 'end_time': 'null', 'title': 'Coding Explanation'}]}
```
## Dataset format
The dataset will be used to finetune a chat model, in this ``TinyLLama``. The dataset format will be:
```python
{
    "instruction": "Extract the timestamps from the given video description",
    "input": """🚀 https://neetcode.io/ - A better way to prepare for Coding Interviews

Solving Removing Stars From a String - Leetcode 2390, today's daily leetcode problem on April 10th.

🥷 Discord: https://discord.gg/ddjKRXPqtk
🐦 Twitter: https://twitter.com/neetcode1

🐮 Support the channel: https://www.patreon.com/NEETcode

⭐ BLIND-75 PLAYLIST: https://www.youtube.com/watch?v=KLlXCFG5TnA&list=PLot-Xpze53ldVwtstag2TL4HQhAnC8ATf
💡 DYNAMIC PROGRAMMING PLAYLIST: https://www.youtube.com/watch?v=73r3KWiEvyk&list=PLot-Xpze53lcvx_tjrr_m2lgD2NsRHlNO&index=1

Problem Link: https://leetcode.com/problems/removing-stars-from-a-string/

0:00 - Read the problem
0:30 - Drawing Explanation
2:45 - Coding Explanation

leetcode 2390

#neetcode #leetcode #python""",
    "output": {'video_id': '6st4IxEF-90',
 'time_stamps': [{'start_time': '0:00',
   'end_time': '0:50',
   'title': 'Read the problem'},
  {'start_time': '0:50', 'end_time': '10:10', 'title': 'Drawing Explanation'},
  {'start_time': '10:10', 'end_time': 'null', 'title': 'Coding Explanation'}]}
```
## Dataset Generation
To extract the time stamps we will use llama8b from Groq, with the help of langchain. We will use the oryks-youtube library to extract video descriptions.
## Usage
This module will be used to generate and store timestamps from:
- One or more videos, given the video title or video id
- One or more playlists given the playlist title and channel name or just the playlist id
- A channel title or id as well as playlist titles
#### Installation
1. Clone the repo:
    ```git clone ```
2. Navigate to the project repo
    ```cd```
3. Create and activatev a virtual environment
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```
4. Install the requirements
    ```pip install -r requirements.txt```
5. Get the youtube api key; follow this tutorial
#### Dataset generation
6. Generate the dataset
    - For a single video with title: (ensure you surround the titles with quotes)
        ```bash
        python -m youtube-timestamps --secret-file /home/lyle/oryks/backend/api/libraries/youtube.json --type videos --names 'Accounts Merge - Leetcode 721 - Python' --GROQ_API_KEY gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        ```

    - For a single video with id
        ```bash
        python -m youtube-timestamps --secret-file /home/lyle/oryks/backend/api/libraries/youtube.json --type videos --ids 6st4IxEF-90 --GROQ_API_KEY gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        ```

    - For a single playlist with id
        ```bash
        python -m youtube-timestamps --secret-file /home/lyle/oryks/backend/api/libraries/youtube.json --type playlists --ids PLQpVsaqBj4RLwXMZ9LaAFf4rVowiC3ZcG --GROQ_API_KEY gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        ```

    - For a single channel with id and playlists ids
        ```bash
        python -m youtube-timestamps --secret-file /home/lyle/oryks/backend/api/libraries/youtube.json --type channels --ids UC8tgRQ7DOzAbn9L7zDL8mLg --playlists_ids PLRzwgpycm-Fi-C7EwEmlSrE0RTX-2Sp06 PLRzwgpycm-FjIPHnCS9q8WH3gjrmbfSgY --GROQ_API_KEY gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        ```
    - For a single channel with name and playlist names
        ```bash
        python -m youtube-timestamps --secret-file /home/lyle/oryks/backend/api/libraries/youtube.json --type channels --names 'John Watson Rooney' --playlists_names 'Playwright & Python', 'Weekly Web Scraping Tips', 'Web Scraping Tips' --GROQ_API_KEY gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        ```

    - For a single channel with name(this will parse all the playlists in the channel)
        ```bash
        python -m youtube-timestamps --secret-file /home/lyle/oryks/backend/api/libraries/youtube.json --type channels --names 'John Watson Rooney' --playlists_ids *  --GROQ_API_KEY gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        ```

#### Dataset generation guidelines
- Always supply the video id instead of the title; when the title is supplied, the module searches for the video which consumes api quotas
- Always supply the playlist id. If you want to supply the playlist title, you must also supply the channel name or title
- When you supply the channel id or title, you can supply the playlist ids or playlist titles. If you do not supply the playlists titles or ids, all the playlists will be parsed. You can only supply a single channel at a time.


