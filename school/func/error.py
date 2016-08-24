# -*- coding: utf-8 -*-

class ErrorPrint:
    @staticmethod
    def printe(name, data, e):
        print("=========="+name+"==========")
        print(data)
        if e!="":
            print("==========except==========")
            print(e)
        print("==========end==========")
