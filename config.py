import os
import platform

TOKEN = "5360699267:AAERB5v0pSG9ngWeJX2BlO3gSlZmjskpmxE"
# TOKEN = "5587049036:AAGKoBH7GlIiv18YKSNeUg74p4CQvr_LvDE"

file_path = os.path.dirname(__file__) + f"\\Products\\files\\" if platform.system() == "Windows" else os.path.dirname(
    __file__) + f"/Products/files/"

pre_view_path = os.path.dirname(__file__) + f"\\Products\\pre_view\\" if platform.system() == "Windows" else os.path.dirname(
    __file__) + f"/Products/pre_view/"
