# json key usami-lab-2d9151da5b90.json
from google.cloud import texttospeech # (1)
from google.cloud import translate_v2 as translate
from transformers import pipeline

import io,sys,time,unicodedata, requests
from argparse import ArgumentParser
from urllib import robotparser
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from ast import literal_eval
from gtts import gTTS
from mutagen.mp3 import MP3 as mp3
import os,socket, pygame, time, pprint

    
def Say2a(data):
    synthesis_input = texttospeech.SynthesisInput(text=data)
    voice = texttospeech.VoiceSelectionParams(
        language_code='ja-JP', # 言語コード
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL )  # 声の希望の性別 
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16 )  # オーディオ種別 

    client = texttospeech.TextToSpeechClient()
    response = client.synthesize_speech(
        input=synthesis_input, # 音声合成入力
        voice=voice, # ボイス設定
        audio_config=audio_config # オーディオ設定
    )

    with open('./examples/sample.wav', 'wb') as out:
#   with open('/home/kita/mak2/examples/sample.wav', 'wb') as out:
        out.write(response.audio_content)

def Say2b(data00):
    #text generator
    print('-------> into text generator-----')
    generator = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B')
    b = generator(data00, do_sample=True, min_length=10,max_length=50,top_p=0.92,top_k=0)
    print('{}'.format(b))
    data = b

    text = [str(i) for i in data]
    h = open('b.txt', 'w', encoding='UTF-8')
    h.write("".join(text))
    h.close()
    
    f = open('b.txt', 'r', encoding='UTF-8')
    c = f.read()
    f.close()
    
    d=c.replace("{'generated_text':", '').replace(r'\n', '').replace('&#39;', '').replace('}', '').replace("'", '')
    e=d.replace('}', '')
    f=d.replace(r'&#39', '')
    g=f.replace("A”}",'')
    
    translate_client=translate.Client()
    a =translate_client.translate(g,target_language='ja')

    #print(result)　＃これでも良い

    print(a['translatedText'])
    doc11=a['translatedText'].split('。')

    nn=len(doc11)-1
    doc22=doc11[0:nn]
    doc33='。'.join(doc22)
    doc44=doc33+'。'

    print(doc44)
   
    hello = doc44
    Say2a(hello)


def check_robots_txt(base_url):
    robots_txt_url = f'{base_url}/robots.txt'
    targets_url = [f'{base_url}/',
                   f'{base_url}/categories/',
                   f'{base_url}/topics/',
                   ]
    user_agent = '*'
    # robots.txtの取得
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_txt_url)
    rp.read()
    time.sleep(1)
    not_list = []
    #各URLがスクレイピング可能かチェックする
    for url in targets_url:
        res = rp.can_fetch(user_agent, f'{url}*')
        if res is False:
            print(f'can not scrape: {url}')
            not_list.append(url)
    return len(not_list) == 0

def get_target_categories(target):
    items = { 'm': '主要', 'd': '国内', 'b': '経済', 'e': 'エンタメ', 'w': '国際' }
    item_list = []
    for k in target:
        item_list.append(items[k])
    return item_list
#-------------------------------
def head_line_long(target):
#-------------------------------
    base_url = 'https://news.yahoo.co.jp/topics/'
    categories = {
        '主要': 'top-picks',
        '国内': 'domestic',
        '経済': 'business',
        'エンタメ': 'entertainment',
        '国際': 'world',
        }
    # カテゴリーごとにループ処理する
    for cat in get_target_categories(target):
        url = urljoin(base_url, categories[cat])
        r = requests.get(url)
        time.sleep(1)
        soup = BeautifulSoup(r.content, 'lxml') # html.parser
        div_tag = soup.find('div', class_='newsFeed')
        if div_tag is None:
            print('div_tag.newsFeed is None.')
            sys.exit()
        ul_tag = div_tag.find('ul', class_='newsFeed_list')

        lll=0
        tx=[]
        for item in ul_tag.find_all('li', class_='newsFeed_item'):
            lll=lll+1
            a = item.find('a')
            if a is None: continue
            topic_url = a['href']

            div_tag = a.find('div', class_='newsFeed_item_title')

            topic_headline = div_tag.text.strip()

            if topic_headline.endswith('オリジナル'):
                topic_headline = topic_headline[:-5]

            text = text_align(topic_headline, 4)
            tx.append(text)
    return tx

def get_han_count(text):
    count = 0
    for char in text:
        if unicodedata.east_asian_width(char) in 'FWA':
            count += 2
        else:
            count += 1
    return count

def text_align(text, width, *, align=-1, fill_char=' '):
    fill_count = width - get_han_count(text)
    if fill_count <= 0: return text
    if align < 0:
        return text + fill_char*fill_count
    else:
        return fill_char*fill_count + text

#-----------------
HOST = '127.0.0.1'    # The remote host
PORT = 50007 # The same port as used by the server
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((HOST, PORT))

import speech_recognition as sr
r = sr.Recognizer()
mic = sr.Microphone()
def Say(data):
    tts=gTTS(data)
    tts.save('answer.mp3')
    tts.save('examples/caffe.wav')
    tts.save('examples/caffe22.wav')
    tts.save('examples/M6_04_16k.wav')
    pygame.mixer.init(frequency=27000)
#   fname='out.mp3'
    fname='answer.mp3'
#   pygame.mixer.music.load(fname)
#   length=mp3(fname).info.length
#   pygame.mixer.music.play(1)
#   time.sleep(length)


#-----------------
def Title(ll):
#-----------------
    tx0=head_line_long('m')
    print('in Title')
    print(ll)
    for i in range(5):
        print(i,tx0[i])
    for j in range(1):
        i=ll
        print('')         
        print(i,tx0[i])
        print('')         

        text=tx0[i]
#        translate_client=translate.Client()
#        a =translate_client.translate(text,target_language='en')


#        header = a['translatedText']
        header = text
        print(header)
        Say2b(header)



#-----------------
ll=0
while True:
    print("Say something ...")
    with mic as source:
        r.adjust_for_ambient_noise(source) #雑音対策
        print("Listening...")
        audio = r.listen(source)
#    print ("Now to recognize it...")
    try:
        print('usami------------------')
        pygame.mixer.init(frequency=27000)

        a=r.recognize_google(audio, language='ja-JP')
        print(a)
        translate_client=translate.Client()
        b =translate_client.translate(a,target_language='en')
        hello = b['translatedText']
        print(hello)
#       hello='What is a band pink floyd'

#       print('============ Query   =================')
#       print('query: {}'.format(hello))
        Say2b(hello)
        print('usami------------------')
        '''
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(hello.encode())
        s.close()
        time.sleep(50)
        '''
        
    except ZeroDivisionError as e:
        print("Error")
        time.sleep(20)
        
