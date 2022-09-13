import os
import platform

TOKEN = ""


file_path = os.path.dirname(__file__) + f"\\Products\\files\\" if platform.system() == "Windows" else os.path.dirname(
    __file__) + f"/Products/files/"

pre_view_path = os.path.dirname(__file__) + f"\\Products\\pre_view\\" if platform.system() == "Windows" else os.path.dirname(
    __file__) + f"/Products/pre_view/"
