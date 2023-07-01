import requests
import time
import json
from pathlib import Path

if __name__ == '__main__':
    api_url = 'http://127.0.0.1:3000/detect/'
    
    req = {
        "imageBase64":None, 
        'imageUrl':None,
        'algCode': None,
        'analysisRule':{
            'baseImage': None,
            'drawFrame': False,
            'screenShot': False,
            'rulesParam': [],
            '---analysisType': [],
            '---area': [],
            '---score': 0.25
        }
    }
    
    '''test1'''
#     req['imageUrl']='https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fss2.meipian.me%2Fusers%2F63682564%2F2a05145aa83e4051851ceeffd9c3e3fe.jpg%3Fmeipian-raw%2Fbucket%2Fivwen%2Fkey%2FdXNlcnMvNjM2ODI1NjQvMmEwNTE0NWFhODNlNDA1MTg1MWNlZWZmZDljM2UzZmUuanBn%2Fsign%2F4028dc85d4f44116465624e860fe2ab1.jpg&refer=http%3A%2F%2Fss2.meipian.me&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1690364841&t=4c063fb1cd7c8dd0cae94a2765f8e955'
    req['imageUrl']='https://img2.baidu.com/it/u=1674838818,207383194&fm=253&fmt=auto&app=138&f=JPEG?w=600&h=415'
    '''test2'''
#     with open('encoded-20230626075554.txt', 'r') as file:
#         imgstr = file.read()
#     req['imageBase64']=imgstr
    
    start = time.time()
    response = requests.post(api_url, json=req)
    print(f'response time: {time.time()-start}')
    print(response.json())
    print(response.status_code)