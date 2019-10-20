from time import sleep
import queue
import threading
#from dataclasses import dataclass

import PySimpleGUI as sg
from faker import Faker


# @dataclass
# class TestItem:
#     name: str
#     limit: str
#     val: float
    
#     def build_list(self):
#         return [self.name,self.limit,self.val]
    


f = Faker()
items = []
limits = []
results = []
for i in range(20):
    items.append(f.name())
    limits.append(f.name())
    results.append('not tested')
leftvals = list(zip(items, limits, results))
rightvals = list(zip(items, limits, results))

gui_queue = queue.Queue()


def data_gen(f,gui_queue):
    gui_queue.put(('data',f.pyfloat(2, 2, False)))
    
def wait_time(desc, secs,gui_queue):
    gui_queue.put(('info', f'{desc} , wait {secs} seconds'))
    gui_queue.put(('wait',-1))
    for i in range(secs, 0, -1):
        gui_queue.put(('wait',i))
        sleep(1)
    gui_queue.put(('wait',0))
    gui_queue.put(('info',f'{desc} , finish'))

def tester_run(gui_queue):
    f=Faker()
    wait_time('open devices', 5, gui_queue)
    
    for i in range(20):
        data_gen(f,gui_queue)
        wait_time(f'test {i+1}', 2, gui_queue)

        



layout = [
    [
        sg.Frame('命令', [[sg.Button('开始测试', key='-START-'), sg.Checkbox('重新校准', key='-RECAL-')]]),
        sg.Frame('工号',[[sg.Input(size=(10,1),key='-TESTOR-')]]),
        sg.Frame('状态',[[sg.Text('空闲中',size=(30,1),key='-STATUS-'),sg.Text('',size=(3,1),visible=False,background_color='Grey',key='-TIMECOUNT-')]]),
        
    ],
    [
        sg.Frame('TX',[[sg.Text('UNKOWN')],[sg.Table(leftvals, headings=['测试项', '有效值', '实际值'] ,num_rows=len(leftvals),alternating_row_color='#9FB8AD',key='-LEFT-')]]),
        sg.Frame('RX',[[sg.Text('UNKOWN')],[sg.Table(rightvals, headings=['测试项', '有效值', '实际值'],num_rows=len(leftvals), key='-RIGHT-')]])
        
    ]
]

window = sg.Window('Tester', layout)

while True:
    event,values = window.read(timeout=100)
    print(event, values)
    if event is None:
        break
    if event == '-START-':
        thread_id = threading.Thread(target=tester_run, args=(gui_queue,), daemon=True)
        thread_id.start()
        needrecal = values['-RECAL-']
        if needrecal is False:
            window['-STATUS-'].update('开始工作')
        else:
            window['-STATUS-'].update('开始校准')
    # if event == '-LEFT-':
    #     window['-STATUS-'].update(values['-LEFT-'][0])
    
    try:
        message = gui_queue.get_nowait()
    except queue.Empty:
        message = None
    if message is not None:
        mtype, content = message
        if mtype == 'wait':
            if content == -1:
                window['-TIMECOUNT-'].update(visible=True)
            elif content == 0:
                window['-TIMECOUNT-'].update(visible=False) 
            else:
                window['-TIMECOUNT-'].update(content)
        elif mtype == 'info':
            window['-STATUS-'].update(content)
        elif mtype == 'data':
            newvals = [ [j[0],j[1],content] for j in leftvals]
            window['-LEFT-'].update(newvals,row_colors=[(3,'lightblue')])

window.close()
        
