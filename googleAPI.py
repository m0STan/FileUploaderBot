from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build

import pprint
import io


SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "C:/Users/Aleksey/PycharmProjects/FileUploaderBot/fileuploaderbot-434821-50b41ddb49e4.json"

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)


def get_disk_list():
    results = service.files().list(pageSize=1000,
                               fields="nextPageToken, files(id, name)").execute()
    return results

def upload_file(file_path):
    name = file_path.split("/")[-1]
    file_path = file_path
    file_metadata = {
        'name': name,
    }
    media = MediaFileUpload(file_path, resumable=True)
    created = service.files().create(body=file_metadata, media_body=media, fields='id,webViewLink').execute()
    print(created)

    # Тело запроса назначения прав
    file_permission = {"role": "writer", "type": "anyone"}

    # Назначение прав
    service.permissions().create(
        body=file_permission, fileId=created.get("id")
    ).execute()
    return created.get("webViewLink")


def clear_disk():
    list = get_disk_list()
    for file in list["files"]:
        service.files().delete(fileId=file['id']).execute()