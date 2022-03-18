'''
Author: your name
Date: 2022-03-17 21:19:48
LastEditTime: 2022-03-17 23:33:44
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /AstroSchedullerGo/Python/main.py
'''

from utilities import utilities
from core import core

u = utilities()
c = core()

print(c.go_schedule("../tests/psr_list_debug.xml", "./export.xml"))