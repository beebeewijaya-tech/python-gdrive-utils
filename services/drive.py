from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io
import os


class DriveService:
  service = ""

  def __init__(self, service):
    self.service = service

  def create_folder(self, folder_name, parent_folder_id=None):
      """Create a folder in Google Drive and return its ID."""
      folder_metadata = {
          'name': folder_name,
          "mimeType": "application/vnd.google-apps.folder",
          'parents': [parent_folder_id] if parent_folder_id else []
      }

      created_folder = self.service.files().create(
          body=folder_metadata,
          fields='id',
          supportsAllDrives=True
      ).execute()

      print(f'Created Folder ID: {created_folder["id"]}')
      return created_folder["id"]

  def upload_file(self, file_path, file_name, mime_type='text/plain', parent_folder_id=None):
    """Upload a file to Google Drive."""
    file_metadata = {
      'name': file_name,
      'parents': [parent_folder_id] if parent_folder_id else []
    }
    media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
    file = self.service.files().create(
    body=file_metadata, media_body=media, fields='id').execute()
    print(f"Uploaded file with ID: {file.get('id')}")

  def search_folder_name(self, folder_name):
    results = (
          self.service.files()
          .list(pageSize=100, fields="nextPageToken, files(id, name, mimeType)", q=f'name = "{folder_name}"')
          .execute()
    )
    items = results.get("files", [])
    return items

  def search_folder_name(self, folder_name):
    results = (
          self.service.files()
          .list(pageSize=100, fields="nextPageToken, files(id, name, mimeType)", q=f'name = "{folder_name}" and mimeType = "application/vnd.google-apps.folder"')
          .execute()
    )
    items = results.get("files", [])
    return items

  def list_files_from_parent_folder(self, parent_folder_id):
    results = (
          self.service.files()
          .list(pageSize=100, fields="nextPageToken, files(id, name, mimeType)", q=f'"{parent_folder_id}" in parents')
          .execute()
    )
    items = results.get("files", [])
    return items


  def copy_file(self, fileId, fileName, parent_folder_id):
    newFile = {"parents": [parent_folder_id], 'name': fileName}
    self.service.files().copy(fileId=fileId, body=newFile).execute()
    print(f"Copying {fileId}-{fileName} into new parent {parent_folder_id}")

  def downloadfiles(self, dowid, name,dfilespath):
      p = dfilespath + "/" + name
      if not os.path.exists(p):
        extFile = name.split('.')

        if len(extFile) <= 1:
          request = self.service.files().export_media(fileId=dowid, mimeType='text/csv')
        else:
          request = self.service.files().get_media(fileId=dowid)

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        with io.open(dfilespath + "/" + name, 'wb') as f:
            fh.seek(0)
            f.write(fh.read())
      else:
        print("skipping because already exist: ", name)
       
