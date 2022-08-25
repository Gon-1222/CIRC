class Gfile():
    ID = os.environ["GOOGLE_ID"]
    scope = ["https://www.googleapis.com/auth/drive"]
    JSON_FILE = "service_key.json"
    def load_file(self,path):
        gauth = GoogleAuth()
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.JSON_FILE, self.scope)
        drive = GoogleDrive(gauth)
        file = drive.CreateFile({"id": path, "parents": [{"id": self.ID}]})
        data=file.GetContentString()
        return json.loads(data)
    def save_file(self,path,contents):
        if not isinstance(contents, list) or not isinstance(contents, dict) :
            return False
        contents=json.dumps(contents)
        gauth = GoogleAuth()
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.JSON_FILE, self.scope)
        drive = GoogleDrive(gauth)
        file = drive.CreateFile({"id": path, "parents": [{"id": self.ID}]})
        file.SetContentString(contents)
        file.Upload()
        return True
