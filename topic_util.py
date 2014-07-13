#coding=utf8

import json,redis,threading
from bs4 import BeautifulSoup,element
from http_util import *


redis_pool = redis.ConnectionPool(host="localhost",port=6379,db=0)


def get_topic_info(topic):
    redis_obj = redis.Redis(connection_pool=redis_pool)
    result_list = []
    original_html = get_topic_response(topic)
    if original_html:
        struct_html = json.loads(original_html)
        topic_info = struct_html['data']['html']
        soup_obj = BeautifulSoup(topic_info,"lxml")
        soup_obj.prettify()
        latest_soup_list = soup_obj.find_all('li',{'node-type':'list-item'})
        latest_soup_list = latest_soup_list[::-1]
        if latest_soup_list:
            print "find latest topic info"
            for latest_soup in latest_soup_list:
                result_dict = {}
                data_attr = latest_soup.attrs.get('list-data')
                if data_attr is not None:
                    data_attr_dict = convert_str2dict(data_attr)
                    message_id = data_attr_dict.get('mid',None)
                    existed_message_id = redis_obj.hget(REDIS_SET,topic)
                    print message_id
                    if existed_message_id and int(message_id) <= int(existed_message_id):
                        continue
                    elif message_id is not None:
                        redis_obj.hset(REDIS_SET,topic,message_id)
                        result_dict['message_id'] = message_id
                        latest_text_soup = latest_soup.find('em',{'node-type':'txt_em'})
                        latest_attached_soup = latest_soup.find('div',{'class':'con_media'})

                        if latest_text_soup is not None:
                            content_list = map(filter_text_info,latest_text_soup.contents)
                            latest_text_info = "".join(content_list)
                            result_dict['context'] = latest_text_info

                        if latest_attached_soup is not None:
                            attached_list = map(filter_media_info,latest_attached_soup.find_all("img"))
                            result_dict['img_src_list'] = attached_list

                        if result_dict:
                            result_list.append(result_dict)
    return result_list


def filter_text_info(content):
    if isinstance(content,element.Tag):
        return content.text

    return content

def filter_media_info(content):
    return content.attrs.get('src',None)

def convert_str2dict(str):
    return dict([entry.split('=') for entry in str.split('&')])


if __name__ == '__main__':
    get_topic_info("你的字体能见人吗")