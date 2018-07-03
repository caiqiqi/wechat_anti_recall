import time
import termcolor

import constant


def color(message, color):
    msg = termcolor.colored(str(message), str(color), attrs=["bold"])
    return msg

def time_now():
    return time.strftime(constant.TIME_FORMAT, time.localtime())

#@pIsToUserName: 消息中是否存在'ToUserName'字段
#
def print_msg_in_format(pMsg_time_receive, pMsg_from_nick, pMsg_to_nick, pPrint_msg, \
    pIsToUserName=True, pIsMsgRecall=False):
    if not pIsMsgRecall:  #若不是撤回消息
        if pIsToUserName:
            print(color('[%s]' % pMsg_time_receive, "grey") + \
                color('[%s ==> %s]: %s' % (pMsg_from_nick, pMsg_to_nick, pPrint_msg), "green"))
        else:
            print(color('[%s]' % pMsg_time_receive, "grey") + \
                color('[%s]: %s' % (pMsg_from_nick, pPrint_msg), "green"))
    else:  #是撤回的消息
        print(color('[%s]' % pMsg_time_receive, "red") + \
            color('[%s](#撤回): %s' % (pMsg_from_nick, pPrint_msg), "red"))
    return