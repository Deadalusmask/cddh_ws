import asyncio
import datetime
import websockets
import requests
import json
import methods
from threading import Thread

questions = []
answer_sets = []

async def send_request():
    resp = requests.get('http://htpmsg.jiecaojingxuan.com/msg/current',timeout=4).text
    try:
        resp_dict = json.loads(resp)
    except json.JSONDecodeError as identifier:
        print('Passed JSONDecodeError')
        return '0'
    
    # print("resp_dict=",resp_dict)
    # print(answer_sets)
    test = 123
    if resp_dict['msg'] == 'no data':
        print('Waiting for question...') 
        return '0'
    else:
        resp_dict = eval(str(resp))
        question = resp_dict['data']['event']['desc']
        question = question[question.find('.') + 1:question.find('?')]
        if question not in questions:
            questions.append(question)
            answers = eval(resp_dict['data']['event']['options'])
            answer_sets.append(answers)
            m2 = Thread(methods.run_algorithm(1, question, answers))
            m3 = Thread(methods.run_algorithm(2, question, answers))
            m2.start()
            m3.start()
            return question+'+'+str(answers)
        else:
            print('Waiting for new question...')
            return '0'

async def producer_handler(websocket, path):
    while True:
        message = await send_request()
        await websocket.send(message)
        await asyncio.sleep(2)

def main():
    start_server = websockets.serve(producer_handler, '127.0.0.1', 5678)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
    

if __name__ == '__main__':
    main()
