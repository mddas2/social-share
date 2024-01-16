class Api:
    def __init__(self):
        self.initial_version = "1.0.0"
        self.version = "1.0.1" #"2.0.0"

        #stand alone "pyinstaller --onefile --icon=images/kantipur.ico  --distpath output_folder login.py"
        # "kitSERVER5@##@d" root password

        self.port = "8004"
        # self.port = "8001"

        base  = "http://64.227.182.105"
        base_websocket = "ws://64.227.182.105"

        # base  = "http://127.0.0.1"
        # base_websocket = "ws://127.0.0.1"

        self.login_api = f"{base}:{self.port}/account/api/login/" 
        self.websocket_api = f"{base_websocket}:{self.port}/ws/"

        self.software_download = f"{base}:{self.port}/version-lists"
        self.get_current_version = f"{base}:{self.port}/get-latest-version"


       