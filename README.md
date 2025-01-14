# Datasets

## Overview

This repository contains the code for generating datasets used in finetuning and training various models. The datasets currently include:

- [YouTube Timestamps Extractor](./youtube-timestamps/) - This is a dataset that is used in the finteuning of a ``TinyLLama`` chat model for extraaction of timestamps from youtube videos. The timestamps are used to separate a video into different sections.
  It consists of a list of dictionaries of ``instruction``, ``input`` and ``output`` keys. Here is a sample:

```python
[
    {
        "instruction": "Extract timestamps from the video description given.",
        "input": "\ud83d\ude80 https://neetcode.io/ - A better way to prepare for Coding Interviews\n\n\ud83e\udd77 Discord: https://discord.gg/ddjKRXPqtk\n\ud83d\udc26 Twitter: https://twitter.com/neetcode1\n\n\ud83d\udc2e Support the channel: https://www.patreon.com/NEETcode\n\n\u2b50 BLIND-75 PLAYLIST: https://www.youtube.com/watch?v=KLlXCFG5TnA&list=PLot-Xpze53ldVwtstag2TL4HQhAnC8ATf\n\ud83d\udca1 DYNAMIC PROGRAMMING PLAYLIST: https://www.youtube.com/watch?v=73r3KWiEvyk&list=PLot-Xpze53lcvx_tjrr_m2lgD2NsRHlNO&index=1\n\nProblem Link: https://leetcode.com/problems/accounts-merge/\n\n0:00 - Read the problem\n0:50 - Drawing Explanation\n10:10 - Coding Explanation\n\nleetcode 721\n\n#neetcode #leetcode #python",
        "output": {
            "video_id": "6st4IxEF-90",
            "time_stamps": [
                {
                    "timestamp": "0:00",
                    "title": "Read the problem"
                },
                {
                    "timestamp": "0:50",
                    "title": "Drawing Explanation"
                },
                {
                    "timestamp": "10:10",
                    "title": "Coding Explanation"
                }
            ]
        }
    }
]
```

To generate timestamps from a playlist:
```bash
python -m youtube-timestamps --secret-file /home/lyle/oryks/backend/api/libraries/youtube.json --type channels --names 'John Watson Rooney' --playlists_names 'Playwright & Python', 'Weekly Web Scraping Tips', 'Web Scraping Tips' --GROQ_API_KEY gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
Then upload the dataset to huggingface:
```python
python upload.py -d youtube-timestamps
```