
#时间格式
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

#消息类型(附件/视频/图片/语音)
DICT_MSG_TYPE = {'Attachment', "Video", 'Picture', 'Recording'}

#朋友聊天消息(正常)
MSG_FRIEND_NORMAL = 0
#朋友聊天消息(撤回)
MSG_FRIEND_RECALL = -1
#附件/视频/图片/语音消息(正常)
MSG_MEDIA_NORMAL = 1
#附件/视频/图片/语音消息(撤回)
MSG_MEDIA_RECALL = 2
#分析的音乐/文章(正常)
MSG_SHARE_NORMAL = 3
#分析的音乐/文章(撤回)
MSG_SHARE_RECALL = 4