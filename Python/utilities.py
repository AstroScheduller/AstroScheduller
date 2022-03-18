'''
Author: your name
Date: 2022-03-17 23:15:37
LastEditTime: 2022-03-17 23:16:51
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /AstroSchedullerGo/Python/utilities.py
'''

import os

class utilities():
    def get_dir(self, filename):
        return os.path.abspath(os.path.dirname(filename))
    