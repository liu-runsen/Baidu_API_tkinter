'''
@Author： Runsen
@WeChat：RunsenLiu
@微信公众号： Python之王
@CSDN： https://blog.csdn.net/weixin_44510615
@Github： https://github.com/MaoliRUNsen
@Date： 2020/11/29
'''

import requests
import base64

class Baidu_API():
    def __init__(self):
        self.headers={'Content-Type': 'application/json; charset=UTF-8'}
        self.AppID = '23061934'  # 百度应用账号ID
        self.APIKey = '0EGiM1wDAH5kmFAvhYVLYCbs'  # 针对接口访问的授权方式
        self.SecretKey = 'KVugHxxu4uq203b111SwVY2w98Cd9D70'  # 密钥

    #获取access token值
    def get_access_token(self):
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(self.APIKey,self.SecretKey)
        response = requests.get(host,self.headers)
        if response:
            access_token=response.json()['access_token']
            return access_token
        else:
            print("access_token获取失败")

    #获取转换图片格式为base64的图片数据
    def get_img_base64(self,img_path):
        # 先以二进制的格式读取图片，再转化为base64格式（使用二进制转base64格式的函数）
        with open(img_path,'rb')as f:
            # base64编码
            img_data = base64.b64encode(f.read())
        return img_data

    #功能1、对颜值进行评分
    def face_detect(self,img_path):
        try:
            # 访问人脸检测api
            base_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
            # 基本参数
            request_url = base_url + "?access_token=" + self.get_access_token()

            params = {"image": self.get_img_base64(img_path),
                      "image_type": "BASE64",
                      "face_field": "faceshape,facetype,beauty,age,beauty,glasses,gender,race"}
            # 开始访问
            response = requests.post(url=request_url,
                                      data=params,
                                      headers=self.headers)
            re = response.json()
            score = re["result"]["face_list"][0]['beauty']
            age = re["result"]["face_list"][0]['age']
            gender = re["result"]["face_list"][0]['gender']['type']
            race = re["result"]["face_list"][0]['race']['type']
            # 返回数据
            print(score,age,gender,race)
            return score,age,gender,race
        except:
            return '未能正确识别，请重试'

    #功能2、手势识别
    def gesture(self,img_path):
        try:
            base_url = 'https://aip.baidubce.com/rest/2.0/image-classify/v1/gesture'
            # 基本参数
            request_url = base_url + "?access_token=" + self.get_access_token()
            params = {"image": self.get_img_base64(img_path),
                      "image_type": "BASE64"}
            # 开始访问
            response = requests.post(url=request_url,
                                     data=params,
                                     headers=self.headers)  # <class 'requests.models.Response'>

            re = response.json()  # <class 'dict'>
            classname_en = re["result"][0]['classname']
            classname_zh = self.translate(classname_en)
            print(classname_en,classname_zh)
            return classname_en,classname_zh
        except:
            return '未能正确是识别，请重试'


    #功能3、人像分割抠图
    def body_seg(self,img_path, out_path):
        try:
            base_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_seg"
            request_url = base_url + "?access_token=" + self.get_access_token()
            params = {"image": self.get_img_base64(img_path)}
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.post(request_url, data=params, headers=headers)
            labelmap = base64.b64decode(response.json()['foreground'])
            with open(out_path, 'wb') as fp:
                fp.write(labelmap)
        except:
            return '未能正确识别，请重试'

    # 翻译APi接口
    def translate(self, query):
        url = 'http://fanyi.youdao.com/translate?&doctype=json&type=AUTO&i={}'.format(query)
        r = requests.post(url=url)
        return r.json()['translateResult'][0][0]['tgt'].strip('的')
