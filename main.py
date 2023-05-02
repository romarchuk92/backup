
with open('token_vk.txt', 'r') as file_object_1:
    access_token_vk = file_object_1.read().strip()

with open('token_ya.txt', 'r') as file_object_2:
    access_token_ya = file_object_2.read().strip()

from pprint import pprint
import requests
import json

# Вводим id пользователя, фото которого планируем сохранить
id_user = '*********'


# Получаем словари пяти фотографий с информацией о размере фото, количестве лайков и ссылки на фото
def avatar (access_token_vk, user_id):
    URL = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id' : user_id,
        'access_token': access_token_vk, 
        'v':'5.131',
        'album_id':'profile',
        'extended':'likes'
    }
    res = requests.get(URL, params).json()
    req = res['response']['items']
    sizes = {}
    size_dict = {'s': 1, 'm': 2, 'o': 3, 'p': 4, 'q': 5, 'r': 6, 'x': 7, 'y': 8, 'z': 9, 'w': 10}
    photo = 1

    for items in req:
        file_url = max(items['sizes'], key=lambda x: size_dict[x["type"]])
        sizes[f'photo_{photo}'] = file_url
        sizes[f'photo_{photo}'].update(items['likes'])
        photo += 1
        if photo > 5:
            break 
    return(sizes)


# Загрузка фото в яндекс диск
class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

# Загружаем фото и создаем папку для загрузки фото       
    def upload(self, disk_file_path: str, url):
        headers = self.get_headers()
        file_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {"path": disk_file_path, "url": url}
        # Создание папки для загрузки фото пользователя
        folder_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        params_folder = {"path": f'Пользователь_id{id_user}'}
        response_folder = requests.put(folder_url, headers=headers, params=params_folder)
        # ---------------------------------------------
        response = requests.post(file_url, headers=headers, params=params)
        if response_folder.status_code == 201:
            print("Folder create")
        if response.status_code == 202:
            print("Photo downloaded")
        else: 
            print("Failure")

# Вывод результата
if __name__ == '__main__':
    
    info_photo = avatar(access_token_vk, id_user)
    info = []
    for url_photo in info_photo.values():
        
        url_vk = url_photo.get('url')
        like_vk = url_photo.get('count')
        size_vk = url_photo.get('type')
        uploader = YaUploader(access_token_ya)
        uploader.upload(f"Пользователь_id{id_user}/{like_vk}.jpeg", url_vk)

    # Создаю словарь с инфой, для записи его в json файл
        info_1 = {}
        info_1['file_name'] = f'{like_vk}.jpeg'
        info_1['size'] = size_vk
        info.append(info_1)
    with open('information.json', 'w', encoding="utf-8") as file:
        json.dump(info, file)
    # -------------------------------------------------










