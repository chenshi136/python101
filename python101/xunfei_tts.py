# -*- coding:utf-8 -*-
# 科大讯飞TTS模块

import websocket
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
import os
import platform
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread

# 导入音频播放库
try:
    import pygame
    pygame.mixer.init(frequency=24000)
    HAS_PYGAME = True
    print("✓ Pygame 已加载")
except Exception as e:
    print(f"⚠ Pygame 未安装，将使用系统默认播放器: {e}")
    HAS_PYGAME = False

# ========== 科大讯飞TTS配置（在这里填写你的API信息）==========
APPID = '6163133a'  # 替换为你的APPID
APIKEY = 'd8930b4a4336a4a6637d85f5f20e4328'  # 替换为你的APIKey
APISECRET = 'NjljZjk2YjQ4ZmQ3OWMxOWJiZDMxYjEx'  # 替换为你的APISecret
REQURL = 'wss://cbm01.cn-huabei-1.xf-yun.com/v1/private/mcd9m97e6'  # 根据你的服务地址修改

# ========== 音频保存配置 ==========
AUDIO_SAVE_DIR = 'tts_audio'  # 音频保存文件夹
SAVE_AUDIO = True  # 是否保存音频文件到本地（True=保存，False=不保存）
# ============================================================

class Ws_Param(object):
    def __init__(self, APPID, APIKey, APISecret, Text):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.Text = Text
        self.CommonArgs = {"app_id": self.APPID, "status": 2}
        self.BusinessArgs = {
            "tts": {
                "vcn": "x5_lingxiaoyue_flow",
                "volume": 60,
                "rhy": 1,
                "speed": 50,
                "pitch": 50,
                "bgs": 0,
                "reg": 0,
                "rdn": 0,
                "audio": {
                    "encoding": "lame",
                    "sample_rate": 24000,
                    "channels": 1,
                    "bit_depth": 16,
                    "frame_size": 0
                }
            }
        }
        self.Data = {
            "text": {
                "encoding": "utf8",
                "compress": "raw",
                "format": "plain",
                "status": 2,
                "seq": 0,
                "text": str(base64.b64encode(self.Text.encode('utf-8')), "UTF8")
            }
        }

def parse_url(requset_url):
    stidx = requset_url.index("://")
    host = requset_url[stidx + 3:]
    schema = requset_url[:stidx + 3]
    edidx = host.index("/")
    if edidx <= 0:
        raise Exception("invalid request url:" + requset_url)
    path = host[edidx:]
    host = host[:edidx]
    return type('Url', (), {'host': host, 'path': path, 'schema': schema})()

def assemble_ws_auth_url(requset_url, method="GET", api_key="", api_secret=""):
    u = parse_url(requset_url)
    host = u.host
    path = u.path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
    authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
        api_key, "hmac-sha256", "host date request-line", signature_sha)
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    values = {
        "host": host,
        "date": date,
        "authorization": authorization
    }
    return requset_url + "?" + urlencode(values)

# TTS全局变量
tts_audio_file = None
tts_complete = False

def on_message(ws, message):
    global tts_audio_file, tts_complete
    try:
        message = json.loads(message)
        code = message["header"]["code"]
        
        if code != 0:
            print(f"❌ TTS API错误代码: {code}, 错误信息: {message.get('header', {}).get('message', '未知错误')}")
            tts_complete = True
            return
        
        if "payload" in message and "audio" in message["payload"]:
            audio = message["payload"]["audio"].get('audio', '')
            if audio:
                audio = base64.b64decode(audio)
                status = message["payload"]['audio']["status"]
                
                with open(tts_audio_file, 'ab') as f:
                    f.write(audio)
                
                if status == 2:
                    print(f"✓ 音频生成完成: {tts_audio_file}")
                    ws.close()
                    tts_complete = True
    except Exception as e:
        print(f"❌ 处理TTS消息时出错: {e}")
        tts_complete = True

def on_error(ws, error):
    global tts_complete
    print(f"❌ WebSocket错误: {error}")
    tts_complete = True

def on_close(ws, close_status_code, close_msg):
    global tts_complete
    tts_complete = True

def on_open(ws, wsParam):
    def run(*args):
        d = {"header": wsParam.CommonArgs,
             "parameter": wsParam.BusinessArgs,
             "payload": wsParam.Data}
        ws.send(json.dumps(d))
        print("✓ TTS请求已发送")
    thread.start_new_thread(run, ())

def play_audio(file_path):
    """播放音频文件"""
    try:
        if HAS_PYGAME:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=24000)
            print(f"🔊 使用Pygame播放音频: {file_path}")
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            clock = pygame.time.Clock()
            while pygame.mixer.music.get_busy():
                clock.tick(10)
            print("✓ 音频播放完成")
        else:
            abs_path = os.path.abspath(file_path)
            system = platform.system()
            print(f"🔊 使用系统播放器播放音频: {abs_path}")
            if system == "Windows":
                os.system(f'start "" "{abs_path}"')
            elif system == "Darwin":
                os.system(f'afplay "{abs_path}"')
            else:
                os.system(f'mpg123 "{abs_path}" 2>/dev/null || mplayer "{abs_path}" 2>/dev/null')
    except Exception as e:
        print(f"❌ 播放音频时出错: {e}")
        try:
            # 备用播放方案
            abs_path = os.path.abspath(file_path)
            system = platform.system()
            print(f"🔊 尝试备用播放方案...")
            if system == "Windows":
                os.system(f'start "" "{abs_path}"')
            elif system == "Darwin":
                os.system(f'afplay "{abs_path}"')
            else:
                os.system(f'mpg123 "{abs_path}" 2>/dev/null || mplayer "{abs_path}" 2>/dev/null')
        except Exception as e2:
            print(f"❌ 备用播放方案也失败: {e2}")

def text_to_speech(text):
    """科大讯飞TTS函数 - 主入口"""
    global tts_audio_file, tts_complete
    try:
        if not text or not text.strip():
            print("⚠ 警告：文本为空，跳过TTS")
            return
            
        print(f"📝 开始TTS转换，文本: {text[:50]}...")
        
        if SAVE_AUDIO:
            if not os.path.exists(AUDIO_SAVE_DIR):
                os.makedirs(AUDIO_SAVE_DIR)
        
        timestamp = int(time.time())
        if SAVE_AUDIO:
            audio_filename = f'tts_{timestamp}.mp3'
            tts_audio_file = os.path.join(AUDIO_SAVE_DIR, audio_filename)
        else:
            tts_audio_file = f'tts_temp_{timestamp}.mp3'
        
        if os.path.exists(tts_audio_file):
            os.remove(tts_audio_file)
        
        tts_complete = False
        wsParam = Ws_Param(APPID, APIKEY, APISECRET, text)
        wsUrl = assemble_ws_auth_url(REQURL, "GET", APIKEY, APISECRET)
        
        ws = websocket.WebSocketApp(wsUrl, 
                                   on_message=on_message, 
                                   on_error=on_error, 
                                   on_close=on_close)
        ws.on_open = lambda ws: on_open(ws, wsParam)
        
        def run_ws():
            try:
                ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
            except Exception as e:
                print(f"❌ WebSocket连接错误: {e}")
                global tts_complete
                tts_complete = True
        
        thread.start_new_thread(run_ws, ())
        time.sleep(0.5)
        
        timeout = 15
        start_time = time.time()
        while not tts_complete and (time.time() - start_time) < timeout:
            time.sleep(0.1)
        
        try:
            ws.close()
        except:
            pass
        
        # 检查文件是否生成成功
        if os.path.exists(tts_audio_file) and os.path.getsize(tts_audio_file) > 0:
            file_size = os.path.getsize(tts_audio_file)
            print(f"✓ 音频文件已生成: {tts_audio_file} (大小: {file_size} 字节)")
            play_audio(tts_audio_file)
            
            if not SAVE_AUDIO:
                time.sleep(1)
                try:
                    if os.path.exists(tts_audio_file):
                        os.remove(tts_audio_file)
                except Exception as e:
                    print(f"⚠ 删除临时文件失败: {e}")
        else:
            print(f"❌ 音频文件生成失败或文件为空: {tts_audio_file}")
            if os.path.exists(tts_audio_file):
                print(f"   文件大小: {os.path.getsize(tts_audio_file)} 字节")
    except Exception as e:
        print(f"❌ TTS函数执行出错: {e}")
        import traceback
        traceback.print_exc()
