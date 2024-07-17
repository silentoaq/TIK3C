import ctypes
import random
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, DisconnectEvent, LiveEndEvent, GiftEvent
import json
import threading
import subprocess
import sys
import os
import psutil
from queue import Queue
import keyboard
import time

#初始化
with open('data.json') as f:
    data = json.load(f)

client: TikTokLiveClient = TikTokLiveClient(unique_id=data['unique_id'])

#連線
@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    os.system("cls" if os.name == "nt" else "clear")
    print(f"Connected to @{event.unique_id} (Room ID: {client.room_id})")

#斷線
@client.on(DisconnectEvent)
async def on_disconnect(_: DisconnectEvent):
    print("Disconnected")

#直播結束
@client.on(LiveEndEvent)
async def on_live_end(_: LiveEndEvent):
    print("Live ended :(")

# 定義各個禮物對應的函數
def Q():
    print("Executing Q function")
    keyboard.press_and_release('q')

def W():
    print("Executing W function")
    keyboard.press_and_release('w')

def E():
    print("Executing E function")
    keyboard.press_and_release('e')

def R():
    print("Executing R function")
    keyboard.press_and_release('r')

def D():
    print("Executing D function")
    keyboard.press_and_release('d')

def F():
    print("Executing F function")
    keyboard.press_and_release('f')

def 移動畫面():
    print("Executing 移動畫面 function")
    keys = ['f6', 'f7', 'f8', 'f9']
    keyboard.press('y')
    time.sleep(0.01)
    keyboard.release('y')
    for key in keys:
        keyboard.press(key)
        time.sleep(0.5)
        keyboard.release(key)
        time.sleep(0.01)
    keyboard.press('y')
    keyboard.release('y')
    time.sleep(0.001)

def 偷看隊友():
    print("Executing 偷看隊友 function")
    keyboard.press('f2')
    time.sleep(0.3)
    keyboard.release('f2')
    keyboard.press('f3')
    time.sleep(0.3)
    keyboard.release('f3')
    keyboard.press('f4')
    time.sleep(0.3)
    keyboard.release('f4')
    keyboard.press('f5')
    time.sleep(0.3)
    keyboard.release('f5')

# 滑鼠不受控
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_ulong), ("y", ctypes.c_ulong)]

def get_mouse_position():
    point = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y

def set_mouse_position(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)

# 非同步移動滑鼠的函數
def move_mouse_smooth(target_x, target_y, steps=100, duration=1):
    current_x, current_y = get_mouse_position()
    delta_x = (target_x - current_x) / steps
    delta_y = (target_y - current_y) / steps

    for i in range(steps):
        current_x += delta_x
        current_y += delta_y
        set_mouse_position(int(current_x), int(current_y))
        time.sleep(duration / steps)

    set_mouse_position(target_x, target_y)

def 滑鼠不受控():
    print("Executing 滑鼠不受控 function")
    target_x = random.randint(0, 1920)
    target_y = random.randint(0, 1080)
    move_mouse_smooth(target_x, target_y)

def 無預警關遊戲():
    print("Executing 無預警關遊戲 function")
    [proc.kill() for proc in psutil.process_iter() if proc.name() == "League of Legends.exe"]
    [proc.kill() for proc in psutil.process_iter() if proc.name() == "LeagueClient.exe"]

def 關機():
    print("Executing 關機 function")
    os.system("shutdown /r /f /t 0")

gift_queues = {
    'GG': (Q, Queue()),
    'Ice Cream Cone': (W, Queue()),
    'Rose': (E, Queue()),
    'Doughnut': (R, Queue()),
    'TikTok': (移動畫面, Queue()),
    'Rosa': (偷看隊友, Queue()),
    'Heart Me': (滑鼠不受控, Queue()),
    'Finger Heart': (滑鼠不受控, Queue()),
    'Paper Crane': (D, Queue()),
    'Little Crown': (F, Queue()),
    'Money Gun': (無預警關遊戲, Queue()),
    'Whale diving': (關機, Queue())
}

def worker(gift_name):
    func, queue = gift_queues[gift_name]
    while True:
        task = queue.get()
        if task is None:
            break
        count = task.get('count', 1)  
        for _ in range(count):
            func()
            time.sleep(0.05)
        queue.task_done()

# 啟動工作者執行緒
for gift_name in gift_queues:
    threading.Thread(target=worker, args=(gift_name,), daemon=True).start()

# 將禮物添加到相應的隊列中
def handle_gift(gift_name, count):
    if gift_name in gift_queues:
        func, queue = gift_queues[gift_name]
        queue.put({'gift_name': gift_name, 'count': count})
    else:
        print(f"Unknown gift: {gift_name}")

def streakableGift(event):
    handle_gift(event.gift.name, event.combo_count)

def nostreakableGift(event):
    handle_gift(event.gift.name, 1)

# 禮物
@client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    if event.gift.streakable:
        if not event.streaking:
            streakableGift(event)
    else:
        nostreakableGift(event)

def 重起():
    os.system("cls" if os.name == "nt" else "clear")
    print("重起...")
    subprocess.Popen([sys.executable] + sys.argv, close_fds=True, shell=True, start_new_session=True)
    os._exit(0)

if __name__ == '__main__':
    keyboard.add_hotkey('=',重起) 
    client.run()
