from nonebot import get_driver
from nonebot import on_command
from nonebot import logger
from nonebot.message import event_preprocessor
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message,Bot,Event
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.exception import IgnoredException
from pathlib import Path
from .config import Config
import json
import re,os,time


__plugin_meta__ = PluginMetadata(
    name="helper_plus",
    description="带有指令调用控制(规则阻断/屏蔽)的高级helper",
    homepage="https://github.com/fR0Z863xF/nonebot-plugin-helper-plus",
    usage="写好配置文件",
    supported_adapters={"~onebot.v11"},
    type="application",
    config=Config,
    extra={"version": "0.1.7"},
)


global_config = get_driver().config
config = Config.parse_obj(global_config)

if not config.config_path.exists():
    os.makedirs(config.config_path)


def proc_time(all_time):
    timenow=time.strftime("%H%M", time.localtime())
    timeA=0
    timeB=0
    timeA+=int(all_time[0])
    timeB+=int(all_time[1])

    if int(timenow) > timeA and int(timenow) < timeB:
        return True
    return False


def is_whitelist(event:GroupMessageEvent,whitelist:dict):
    global config
    msg = event.message.extract_plain_text().strip().split(" ")[0]

    #命令处理
    for i in global_config.command_start:
        if len(whitelist.get("command")) == 0:
            break
        if msg.startswith(i) and msg[1:] in whitelist.get("command"):
            return True
    #消息处理
    for j in whitelist.get("regex"):
        if re.match(j,msg[1:]) or re.match(j,msg):
            return True

    #命令处理（时段）
    
    for i in global_config.command_start:
        if len(whitelist.get("command")) == 0:
            break
        if msg.startswith(i):
            for j in whitelist.get("time_span").keys():
                if proc_time(j.split("-")):
                    if msg[1:] in whitelist.get("time_span").get(j).get("command"):
                        return True

    #消息处理（时段）
    for i in whitelist.get("time_span").keys():
        
        if proc_time(i.split("-")):
            for j in whitelist.get("time_span").get(i).get("regex"):
                if re.match(j,msg[1:]) or re.match(j,msg):
                    return True
    return False


def is_blacklist(event:GroupMessageEvent,blacklist:dict):
    
    
    global config
    msg = event.message.extract_plain_text().strip().split(" ")[0]

    #命令处理
    for i in global_config.command_start:
        if len(blacklist.get("command")) == 0:
            break
        if msg.startswith(i) and msg[1:] in blacklist.get("command"):
            return True
    #消息处理
    for j in blacklist.get("regex"):
        if re.match(j,msg[1:]) or re.match(j,msg):
            return True

    #命令处理（时段）
    
    for i in global_config.command_start:
        if len(blacklist.get("command")) == 0:
            break
        if msg.startswith(i):
            for j in blacklist.get("time_span").keys():
                #allow_time=blacklist.get("time_span").get(j)
                if proc_time(j.split("-")):
                #if proc_time(allow_time.split("-")):
                    if msg[1:] in blacklist.get("time_span").get(j).get("command"):
                        return True

    #消息处理（时段）
    for i in blacklist.get("time_span").keys():
        
        if proc_time(i.split("-")):
            for j in blacklist.get("time_span").get(i).get("regex"):
                if re.match(j,msg[1:]) or re.match(j,msg):
                    return True
    return False
    


@event_preprocessor
async def do_something(event: GroupMessageEvent,bot: Bot):
    #print(event.group_id)
    #print(config.rule_group)
    if str(event.group_id) in config.rule_group and (config.config_path / (str(event.group_id)+".json")).exists():
        with open(config.config_path / (str(event.group_id)+".json"),"r",encoding="utf-8") as fp:
            rulelist=json.load(fp)
        if rulelist.get("mode") == "whitelist":
            if not is_whitelist(event,rulelist.get("whitelist")):
                raise IgnoredException(str(event.group_id)+"此群已屏蔽此指令")
        elif rulelist.get("mode") == "blacklist":
            if is_blacklist(event,rulelist.get("blacklist")):
                raise IgnoredException(str(event.group_id)+"群已屏蔽此指令")

        else:
            pass


Helper = on_command("help",aliases={'help','帮助'},priority=5)

@Helper.handle()
async def _(bot: Bot, event: Event):
    if str(event.group_id) in config.rule_group:
        if (config.config_path / (str(event.group_id)+".json")).exists():
            with open(config.config_path / (str(event.group_id)+".json"),'r',encoding = 'utf-8') as fp:
                dat=json.load(fp)
        else:
            logger.warning("未找到该群配置文件，使用默认配置。")
            with open(config.config_path / "config.json",'r',encoding = 'utf-8') as fp:
                dat=json.load(fp)
    else:
        if not (config.config_path / "config.json").exists():
            await Helper.finish("未配置帮助信息")
        with open(config.config_path / "config.json",'r',encoding = 'utf-8') as fp:
            dat=json.load(fp)
    i=0
    str_out=''
    for hel in dat["plugins"]:
        i+=1
        str_out+=str(i)+"."+hel["name"]+"\n      "+hel["info"]+"\n"
    await Helper.finish(str_out)
