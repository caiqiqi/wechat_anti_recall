#coding=utf-8
# Python查看微信撤回消息

import re
import os
import json
import platform
import itchat
from itchat.content import TEXT
from itchat.content import *

import util
import constant

msg_info = {}
face_package = None
print_msg = ''

# 处理接收到的信息（只打印朋友聊天的信息，就不要公众号的信息了）
@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True)
def handleRMsg(pMsg):
    global face_package
    global print_msg
    # 接收消息的时间
    _msg_time_receive = util.time_now()
    # 发信人
    try:
        _msg_from = itchat.search_friends(userName=pMsg['FromUserName'])['NickName'] # 发信人的昵称
    except:
        _msg_from = u'微信官方帐号'
    # 信息ID
    _msg_id = pMsg['MsgId']
    _msg_content = None
    _msg_link = None
    _msg_from_nick = ""
    _msg_to_nick   = ""
    # 文本或者好友推荐
    if pMsg['Type'] == 'Text' or pMsg['Type'] == 'Friends':
        _msg_content = pMsg['Text']
        #待打印的字符串
        print_msg = _msg_content
        
    # 附件/视频/图片/语音
    elif pMsg['Type'] in constant.DICT_MSG_TYPE:
        _msg_content = pMsg['FileName']  #消息内容就只给出文件名
        pMsg['Text'](str(_msg_content))
        print_msg = str('[#附件|视频|图片|语音]: %s' % _msg_content)

    # 推荐名片
    elif pMsg['Type'] == 'Card':
        _msg_content = pMsg['RecommendInfo']['NickName'] + '的推荐名片，'
        if pMsg['RecommendInfo']['Sex'] == 1:
            _msg_content += '性别男。'
        else:
            _msg_content += '性别女。'
        print_msg = str('[#名片]: %s' % _msg_content)

    # 位置信息
    elif pMsg['Type'] == 'Map':
        x, y, location = re.search("<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", pMsg['OriContent']).group(1, 2, 3)
        if location is None:
            _msg_content = r"纬度:" + x.__str__() + ", 经度:" + y.__str__()
        else:
            _msg_content = r"" + location
        print_msg = str('[#地图]: %s' % _msg_content)
    # 分析的音乐/文章
    elif pMsg['Type'] == 'Sharing':
        _msg_content = pMsg['Text']
        _msg_link = pMsg['Url']
        print_msg = str('[#分享]: %s \n%s' % (_msg_content, _msg_link))
    

    _msg_from_nick = itchat.search_friends(userName=pMsg['FromUserName'])['NickName']
    if itchat.search_friends(userName=pMsg['ToUserName']):
        try:
            _msg_to_nick   = itchat.search_friends(userName=pMsg['ToUserName'])['NickName']
            util.print_msg_in_format(_msg_time_receive, _msg_from_nick, _msg_to_nick, print_msg, True)
        except Exception as e:
            raise e
    else:
        util.print_msg_in_format(_msg_time_receive, _msg_from_nick, _msg_to_nick, print_msg, False)


    msg_info.update(
            {
                _msg_id: {
                    "msg_from": _msg_from,
                    "msg_time_receive": _msg_time_receive,
                    "msg_type": pMsg["Type"],
                    "msg_content": _msg_content,
                    "msg_link": _msg_link
                }
            }
        )
    face_package = _msg_content


# 监听是否有消息撤回（朋友聊天的，可选 群里的）
@itchat.msg_register(NOTE, isFriendChat=True) #, isGroupChat=True)
def monitor(msg):
    global print_msg
    if '撤回了一条消息' in msg['Content']:
        _recall_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
        _recall_msg = msg_info.get(_recall_msg_id)
        print_msg = _recall_msg.get("msg_content")
        util.print_msg_in_format(util.time_now(), _recall_msg.get('msg_from'), '', print_msg, False, True)
        # 表情包
        if len(_recall_msg_id) < 11:
            itchat.send_file(face_package, toUserName='filehelper')
        else:
            # 准备好撤回消息的内容和格式
            msg_prime = '---' + _recall_msg.get('msg_from') + '撤回了一条消息---\n' \
                        '消息类型：' + _recall_msg.get('msg_type') + '\n' \
                        '时间：' + _recall_msg.get('msg_time_receive') + '\n' \
                        r'内容：' + _recall_msg.get('msg_content')
            if _recall_msg['msg_type'] == 'Sharing':
                msg_prime += '\n链接：' + _recall_msg.get('msg_link')
            # 将该格式的撤回消息发送到文件传输助手
            itchat.send_msg(msg_prime, toUserName='filehelper')
            if _recall_msg['msg_type'] in constant.DICT_MSG_TYPE:
                file = '@fil@%s' % (_recall_msg['msg_content'])
                itchat.send(msg=file, toUserName='filehelper')
                os.remove(_recall_msg['msg_content'])
            msg_info.pop(_recall_msg_id)

if __name__ == '__main__':
    try:
        itchat.auto_login(enableCmdQR=False, hotReload=True)
    except Exception as e:
        raise e
    itchat.run()