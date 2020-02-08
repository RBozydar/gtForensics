import os
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from modules.utils.takeout_html_parser import TakeoutHtmlParser

logger = logging.getLogger('gtForensics')

class MyActivityYouTube(object):
    def parse_youtube_log_body(dic_my_activity_youtube, youtube_logs):
        list_youtube_event_logs = TakeoutHtmlParser.find_log_body(youtube_logs)
        if list_youtube_event_logs != []:
            idx = 0
            for content in list_youtube_event_logs:
                # print("----------------------------------------------")
                content = str(content).strip()
                content = content.replace(u'\xa0', ' ')
                # print(content)
                if idx == 0:
                    if content == 'Searched for':
                        dic_my_activity_youtube['type'] = 'Search'
                    elif content == 'Watched':
                        dic_my_activity_youtube['type'] = 'Watch'
                    elif content == 'Watched a video that has been removed':
                        dic_my_activity_youtube['type'] = 'Watch'
                        dic_my_activity_youtube['keyword'] ='Watched a video that has been removed'
                    elif content == 'Visited YouTube Music':
                        dic_my_activity_youtube['type'] = 'Visit'
                        dic_my_activity_youtube['keyword'] ='Visited YouTube Music'
                    else:
                        # print("!!! ", content)
                        dic_my_activity_youtube['type'] = content
                else:
                    if idx == 1:
                        if content.startswith('<a href="'):
                            idx = content.find('">')
                            dic_my_activity_youtube['url'] = content[9:idx]
                            dic_my_activity_youtube['keyword'] = content[idx+2:content.find('</a>')]
                    else:
                        if dic_my_activity_youtube['type'] == 'Watch':
                            if content.startswith('<a href="'):
                                idx = content.find('">')
                                dic_my_activity_youtube['channel_url'] = content[9:idx]
                                dic_my_activity_youtube['channel_name'] = content[idx+2:content.find('</a>')]
                        if content.endswith('UTC'):
                            dic_my_activity_youtube['timestamp'] = TakeoutHtmlParser.convert_datetime_to_unixtime(content)
                idx += 1

#---------------------------------------------------------------------------------------------------------------
    def parse_youtube(case):
        print('youtube')
        file_path = case.takeout_my_activity_youtube_path
        with open(file_path, 'r', encoding='utf-8') as f:
            file_contents = f.read()
            soup = BeautifulSoup(file_contents, 'lxml')
            # soup = BeautifulSoup(f, 'html.parser')
        #     print("1111111")
            list_youtube_logs = TakeoutHtmlParser.find_log(soup)
            if list_youtube_logs != []:
                for youtube_logs in list_youtube_logs:
                    # print("..........................................................................")
                    # print(youtube_logs)
                    dic_my_activity_youtube = {'type':"", 'url':"", 'keyword':"", 'channel_url':"", 'channel_name':"", 'timestamp':""}
                    MyActivityYouTube.parse_youtube_log_body(dic_my_activity_youtube, youtube_logs)
                    # if dic_my_activity_youtube['type'] == 'Visited YouTube Music':
                        # print("..........................................................................")
                    print(dic_my_activity_youtube)
