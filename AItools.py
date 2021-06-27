import os
import warnings
import random
import uuid
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
warnings.filterwarnings('ignore')

import numpy as np
# import albumentations as alb
# from tensorflow.keras.preprocessing.image import img_to_array, load_img
# from tensorflow.keras.applications import ResNet50, InceptionV3, VGG16, resnet50, inception_v3, vgg16
# from keras.applications.imagenet_utils import decode_predictions

from PIL import Image, ImageDraw, ImageFont
import cv2
import pytesseract

import speech_recognition as sr
import wave

from gtts import gTTS


from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer



# class ImageClassification:

#     def __init__(self, model_name='Resnet'):

#         self.model_name = model_name
#         self.sizes= [224, 229, 224]
        
#         if self.model_name=='Resnet':
#             self.height = self.width = self.sizes[0]
#             weight_dir = 'weights/resnet/resnet50_weights_tf_dim_ordering_tf_kernels.h5'
#             self.model = ResNet50(pooling='avg',  weights=weight_dir)
#         elif self.model_name == 'Inception':
#             self.height = self.width = self.sizes[1]
#             weight_dir = 'weights/inception/inception_v3_weights_tf_dim_ordering_tf_kernels.h5'
#             self.model = InceptionV3(pooling='avg', weights=weight_dir)
#         elif self.model_name == 'Vgg16':
#             self.height = self.width = self.sizes[2]
#             weight_dir = 'weights/vgg16/vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5'
#             self.model = VGG16(pooling='avg', weights=weight_dir)


#     def changemodel(self, model_name=None):
#         if model_name in ['Resnet', 'Inception', 'Vgg16']:
#             self = self(model_name)


#     def read_process_image(self, image_path):
#         image_array = img_to_array(load_img(image_path, target_size=(self.width, self.height)))
#         aug = alb.Compose([
#             alb.Resize(self.height, self.width),
#             #alb.Normalize()
#         ])
#         # image_array = aug(image=image_array)['image']
#         image_array = np.expand_dims(image_array, axis=0)
        
#         if self.model_name=='Resnet':
#             self.image = resnet50.preprocess_input(image_array)
#         elif self.model_name == 'Inception':
#             self.image = inception_v3.preprocess_input(image_array)
#         elif self.model_name == 'Vgg16':
#             self.image = vgg16.preprocess_input(image_array)
    
#     def predict(self):
#         predictions = self.model.predict(self.image)
#         return [(i[1], i[2]) for i in decode_predictions(predictions, top=3)[0]]
# @r0dn3y_




class OCR:

    def __init__(self) -> None:
        pass
    def text_from_image(self, img_path) -> str:
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        gray, img_bin = cv2.threshold(gray,128,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        gray = cv2.bitwise_not(img_bin)
        kernel = np.ones((2, 1), np.uint8)
        img = cv2.erode(gray, kernel, iterations=1)
        img = cv2.dilate(img, kernel, iterations=1)
        out_str = pytesseract.image_to_string(img)
        return out_str



class CreateImage():

    def __init__(self):
        pass

    def draw(self, bgcolor, width, height, text=None, text_col='white') -> None:
        try:
            img = Image.new('RGB', (width, height), color=bgcolor)
        except:
            img = Image.new('RGB', (width, height), color='black')
        _font = random.choice(os.listdir('fonts'))
        fnt = ImageFont.truetype(f"fonts/{_font}", 60)
        if text != None:
            d = ImageDraw.Draw(img)
            try:
                d.text((10, 10), text, font=fnt, fill=text_col)
            except:
                d.text((10, 10), text, font=fnt,  fill='white')
        uuud = str(uuid.uuid1())
        os.mkdir(f'trash/{uuud}')
        file_path = f"trash/{uuud}/temp.png"
        img.save(file_path)    
        return file_path

        # mcolors.to_rgb(text_col)
        # cv2.imshow('image',self.img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # cv2.imwrite('temp.png', cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR))  




class SpeechRecognition:

    def __init__(self):
        pass

    def text_from_audio(self, audio_dir:str) -> str:
        r = sr.Recognizer()
        converted = False
        if audio_dir.split('.')[-1] != 'wav':
            os.system(f'audioconvert convert {audio_dir[:-9]}/ {audio_dir[:-9]}/ --output-format .wav')
            converted = True
            # with open(audio_dir, "rb") as inp_f:
            #     data = inp_f.read()
            #     new_audio_dir = audio_dir.split('.')[0]+'.wav'
            #     with wave.open(new_audio_dir, "wb") as out_f:
            #         out_f.setnchannels(1)
            #         out_f.setsampwidth(2) # number of bytes
            #         out_f.setframerate(44100)
            #         out_f.writeframesraw(data)
            #     audio_dir = new_audio_dir
        audio_dir = audio_dir[:-4]+'.wav'
        with sr.AudioFile(audio_dir) as source:
            # listen for the data (load audio to memory)
            audio_data = r.record(source)
            # recognize (convert from speech to text)
            text = r.recognize_google(audio_data)
            if converted:
                 os.system(f'rm -rf {audio_dir}')
            return text


            
class CreateAudio:

    def __init__(self) -> None:
        pass 
    
    def text_to_audio(self, text, lang='en') -> None:
        myobj = gTTS(text=text, lang=lang, slow=False)
        uuud = str(uuid.uuid1())
        os.mkdir(f'trash/{uuud}')
        ran_path =f"trash/{uuud}/temp.mp3"
        myobj.save(ran_path)
        return ran_path

    
class ChatBott:
    def __init__(self) -> None:
        pass
    def createbot(self):
        chatbot = ChatBot(
            'Jonny',
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database_uri='sqlite:///db.sqlite3'
        )
        return chatbot

