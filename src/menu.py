#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
   构建菜单
"""
import npyscreen


class DBViewerMenu(object):
    def __init__(self, form):
        self.form = form
        self.menu = self.form.new_menu(name='menu')
        self.menu.addNewSubmenu("新建渠道").addItemsFromList([
            ("CIP", self.switchDB, None, None, ('MYBATIS',)),
            ("CAP", self.switchDB, None, None, ('MYBATIS',)),
            ("TPP", self.switchDB, None, None, ('MYBATIS',)),
        ])
        self.menu.addNewSubmenu("原始渠道").addItemsFromList([
            ("XIP", self.switchDB, None, None, ('MYBATIS1',)),
            ("CNAPS2", self.switchDB, None, None, ('MYBATIS1',)),
            ("CUPS", self.switchDB, None, None, ('MYBATIS1',)),
            ("TIPS", self.switchDB, None, None, ('MYBATIS1',)),
            ("MIDL", self.switchDB, None, None, ('MYBATIS1',))
        ])
        self.menu.addItemsFromList([
            ("核心系统", self.whenDisplayText, None, None, ("显示文本",)),
            ("中间业务", self.whenJustBeep),
            ("退出应用", self.exit_application),
        ])

    def whenDisplayText(self, argument):
        npyscreen.notify_confirm(argument)

    def switchDB(self, dbName):
        self.form.dbName.value = dbName
        self.form.init()

    def whenJustBeep(self):
        npyscreen.notify_confirm(str(self.form.tbList.values))

    def exit_application(self):
        self.form.exit_application(ask=False)

class KubernetesMenu(object):
    pass
