#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
   运维工具箱
"""
import curses
import npyscreen
from menu import DBViewerMenu
from pager import Pager
from db import DB
from log import logging
import time


class MainForm(npyscreen.FormBaseNewWithMenus):

    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)
        self.db = None
        self.init()

    def init(self):
        self.sqlTxt.values = []
        self.tbName.value = ''
        self.pageInfo.value = ''
        self.tbData.reset()
        try:
            self.dbClose()
            self.dbOpen(self.dbName.value)
            self.tbList.show()
            self.dbName.value = self.db.dbName
        except BaseException as e:
            logging.error(e)
            npyscreen.notify_confirm(self.db.dbName + str(e))
            self.dbClose()

    def dbOpen(self, dbName):
        self.db = DB(dbName)
        self.db.open()

    def dbClose(self):
        if self.db:
            self.db.close()

    def exit_application(self, ask=True):
        if ask:
            what_to_display = 'Are You Sure To Exit ?'
            result = npyscreen.notify_yes_no(what_to_display)
        else:
            result = True
        if result:
            self.dbClose()
            self.parentApp.setNextForm(None)
            self.parentApp.editing = False
            self.parentApp.switchFormNow()

    def create(self):
        # 获取终端尺寸
        y, x = self.useable_space()

        self.menu = DBViewerMenu(self)
        self.tbList = self.add(TbListBox, name='tables(^t)', relx=1, rely=1, max_height=-9, max_width=x // 7,
                               scroll_exit=False)
        self.dbName = self.add(npyscreen.Textfield,
                               relx=x // 7 + 3, rely=1, editable=False)
        self.tbName = self.add(npyscreen.Textfield,
                               relx=x // 2, rely=1, editable=False)
        self.pageInfo = self.add(
            npyscreen.Textfield, relx=-15, rely=1, editable=False)
        self.tbData = self.add(TbDataBox, name='data(^v)', relx=x // 7 + 3, rely=3, max_height=-12,
                               on_select_callback=None, editable=False, column_width=20, col_margin=1, scroll_exit=False, select_whole_line=True)
        self.inType = self.add(InTypeBox, name='type(^a)', relx=1, rely=-11, max_width=x // 7, max_height=6, scroll_exit=False, value=[0, ], values=['where', 'sql', 'file'])
        self.sqlTxt = self.add(SqlTxtBox, name='sql(^s)', relx=x // 7 + 3, rely=-11, scroll_exit=False)
        self.maxRows = self.add(MaxRowsBox, name='rows(^e)', relx=1, rely=-5, max_width=x // 7, scroll_exit=False, value='100')

        # 定义处理器
        self.add_handlers({
            '^S': lambda input: self.sqlTxt.edit(),  # 编辑SQL
            '^A': lambda input: self.inType.edit(),  # 编辑SQL输入类型
            '^E': lambda input: self.maxRows.edit(),  # 编辑SQL输入类型
            '^T': lambda input: self.tbList.edit(),  # 编辑表名
            '^V': lambda input: self.tbData.edit(),  # 编辑表数据
            '^P': lambda input: npyscreen.blank_terminal(),  # 刷新屏幕
            '^Q': lambda input: self.exit_application()  # 退出应用
        })
        self.tbData.add_handlers({
            curses.ascii.NL: lambda input: self.detailShow(),
            '^F': lambda input: self.tbData.pageDown(),
            '^B': lambda input: self.tbData.pageUp(),
        })
        self.inType.entry_widget.add_handlers({
            # curses.ascii.NL: lambda input: npyscreen.notify_confirm(str(self.inType.entry_widget.value))
            curses.ascii.NL: lambda input: self.selSqlFile()
        })
        self.sqlTxt.add_handlers({
            '^R': lambda input: self.exeSql()
        })

    def exeSql(self):
        sqlTxt = ''
        for value in self.sqlTxt.values:
            sqlTxt = '{0} {1}'.format(sqlTxt, value)

        if self.inType.entry_widget.value[0] == 0:
            if self.tbName.value is None or len(self.tbName.value) == 0:
                npyscreen.notify_confirm('Please Choice The Table First!')
                return
            sql = '''SELECT * FROM {0}.{1} WHERE {2}'''.format(
                self.db.prename, self.tbName.value, sqlTxt).lower()
            confirm = False
        else:
            confirm = True
            sql = sqlTxt.lower()

        try:
            logging.info('sql=[{0}]'.format(sql))
            fromSql = sql[sql.find('from'):]
            logging.info('fromSql=[{0}]'.format(fromSql))
            cntSql = 'select count(*) '+ fromSql
            dataSql = 'select * '+ fromSql
            logging.info('cntSql=[{0}]'.format(cntSql))
            logging.info('dataSql=[{0}]'.format(dataSql))
            self.tbData.init(cntSql)
            self.tbData.show(dataSql, confirm)
        except BaseException as e:
            return

    def selSqlFile(self):
        starting_value = '/Users/zhouyongwei/PycharmProjects/toolbox/tips'
        file = npyscreen.selectFile(starting_value, select_dir=False, must_exist=False, confirm_if_exists=True,
                                    sort_by_extension=True)
        # 如果后缀不是.sql 不读取和赋值
        self.sqlTxt.values = [file]
        self.sqlTxt.edit()

    def detailShow(self):
        self.detailForm = self.parentApp.getForm('RECORD')
        self.detailForm.show(self.tbData.col_titles, self.tbData.selected_row())
        self.parentApp.switchForm('RECORD')

class RecordForm(npyscreen.Form):

    def afterEditing(self):
        self.parentApp.setNextForm('MAIN')

    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)
        self.__options = npyscreen.OptionList().options

    def clear(self):
        self.__options = []
        self._clear_all_widgets()

    def show(self, titles, values):
        self.clear()
        for title, value in zip(titles, values):
            logging.info('title:'+title)
            logging.info('value:'+str(value))
            self.__options.append(npyscreen.OptionFreeText(title, value=value))
        self.add(npyscreen.OptionListDisplay, values=self.__options, scroll_exit=False, max_height=None)
        self.display()
        npyscreen.blank_terminal()

class ListBox(npyscreen.MultiLineAction):
    def actionHighlighted(self, act_on_this, key_press):
        self.parent.tbName.value = act_on_this
        self.parent.tbName.update()
        sql = '''SELECT {0} FROM {1}.{2}'''.format(
            '{0}', self.parent.db.prename, self.parent.tbName.value)
        self.parent.tbData.init(sql.format('count(*)'))
        self.parent.tbData.show(sql.format('*'))


class TbListBox(npyscreen.BoxTitle):
    _contained_widget = ListBox

    def show(self):
        if self.parent.db.type.lower() == 'mysql':
            self.parent.db.cursor.execute('show tables')
        elif self.parent.db.type.lower() == 'oracle':
            self.parent.db.cursor.execute(
                '''select table_name from all_tables where owner = \'{0}\' order by table_name'''.format(self.parent.db.prename))
        self.values = list(map(lambda x: x[0].lower(), self.parent.db.cursor.fetchall()))
        self.update()


class InTypeBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.SelectOne


class MaxRowsBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.Textfield


class SqlTxtBox(npyscreen.MultiLineEditableBoxed):
    pass


class TbDataBox(npyscreen.GridColTitles):
    #_contained_widgets    = npyscreen.Textfield

    def __init__(self, screen, col_titles=None, *args, **keywords):
        super().__init__(screen, col_titles=None, *args, **keywords)

    def init(self, cntSql):
        try:
            self.parent.db.cursor.execute(cntSql)
        except BaseException as e:
            logging.error('Init Valid Sql : ' + cntSql)
            logging.error(e)
            npyscreen.notify_confirm('Valid Sql : ' + cntSql)
            raise e
        self.totalRows = int(self.parent.db.cursor.fetchone()[0])
        logging.info('总条数[%d]' % self.totalRows)
        self.pager = Pager(self.totalRows, int(
            self.parent.maxRows.entry_widget.value))
        self.parent.pageInfo.value = '{0},{1}/{2}'.format(
            self.pager.begRow + 1, self.pager.endRow, self.totalRows)
        self.parent.pageInfo.update()

    def show(self, inSql=None, confirm=False):
        if inSql is not None:
            self.inSql = inSql
        if self.parent.db.type.lower() == 'oracle':
            self.sql = ''' SELECT * FROM ( SELECT ROWNUM NO,A.* FROM ({2}) A WHERE ROWNUM <= {1} ) WHERE NO > {0} '''.format(
                self.pager.begRow, self.pager.endRow, self.inSql)
        elif self.parent.db.type.lower() == 'mysql':
            self.sql = self.inSql   # mysql需要分页
        message = 'Please Check Sql : \n' + self.sql
        if confirm and not npyscreen.notify_ok_cancel(message, title='SQL'):
            return
        try:
            self.parent.db.cursor.execute(self.sql)
        except BaseException as e:
            logging.error('Show Valid Sql : ' + cntSql)
            npyscreen.notify_confirm('Valid Sql : ' + self.sql)
            raise e
        self.values = self.parent.db.cursor.fetchall()
        self.col_titles = list(
            map(lambda x: x[0], self.parent.db.cursor.description))
        self.editable = True
        self.update()
        npyscreen.blank_terminal()
        self.parent.pageInfo.value = '{0},{1}/{2}'.format(
            self.pager.begRow + 1, self.pager.endRow, self.totalRows)
        self.parent.pageInfo.update()
        self.parent.parentApp.switchForm('MAIN')

    def reset(self):
        self.values = []
        self.col_titles = []
        self.update()
        self.editable = False

    def pageDown(self):
        self.pager.down()
        self.show()

    def pageUp(self):
        self.pager.up()
        self.show()

    def custom_print_cell(self, actual_cell, cell_display_value):
        if cell_display_value == 'CN':
            actual_cell.color = 'DANGER'
        elif cell_display_value == 'US':
            actual_cell.color = 'GOOD'
        else:
            actual_cell.color = 'DEFAULT'


class Application(npyscreen.NPSAppManaged):
    def __init__(self):
        super(Application, self).__init__()

    def onStart(self):
        logging.info('进入应用')
        self.addForm('MAIN', MainForm, name='DBViewer', lines=0, columns=0, minimum_lines=24, minimum_columns=80)
        self.addForm('RECORD', RecordForm, name='Record', lines=0, columns=0, minimum_lines=24, minimum_columns=80)
        #self.addForm('BANK', npyscreen.FormBaseNew, name='Blank', lines=0, columns=0, minimum_lines=24, minimum_columns=80)
        self.addForm('MAIN1', TestForm, name='Test', lines=0, columns=0, minimum_lines=24, minimum_columns=80)

    def onInMainLoop(selfs):
        logging.info('in onInMainLoop')

    def onCleanExit(self):
        logging.info('退出应用')

# for test


class TestForm(npyscreen.FormBaseNew):

    def create(self):
        self.add(npyscreen.Textfield, value='Textfield')
        self.add(npyscreen.TitleText, name='TitleText')
        self.add(npyscreen.FixedText, value='FixedText')
        self.add(npyscreen.TitleFixedText, name='TitleFixedText', value='TitleFixedText')
        #self.page = self.add(npyscreen.BufferPager,maxlen=5)
        # for i in range(100):
        #    logging.info("Start : {0}".format(time.ctime()))
        #    logging.info("End : {0}".format(time.ctime()))
        #    self.page.buffer([i])
        self.add(npyscreen.TitleDateCombo, name='日期')
        self.add(npyscreen.TitleCombo, name='TitleCombo', values=['a', 'b', 'c'])
        self.add(npyscreen.TitleFilenameCombo, name='选择文件', select_dir=False, must_exist=False, confirm_if_exists=False, sort_by_extension=True)
        #self.add(npyscreen.TitleSlider, name='TitleSlider', out_of=100,step=1,lowest=0,label=True,value=5)
        #self.add(npyscreen.TitleSliderPercent, name='TitleSliderPercent', out_of=100,step=1,lowest=0,label=True,value=5)
        #self.add(npyscreen.RoundCheckBoxMultiline, name=['a','b','c'], values=['1','2','3'])
        self.add(npyscreen.Button, name='Button')
        self.add(npyscreen.ButtonPress, name='Button')


if __name__ == '__main__':
    App = Application().run()
    '''
    config = configparser.ConfigParser(allow_no_value=True)
    config.read('db.ini', encoding='utf-8')
    username = config.get('CIP', 'servicename')
    print(username)
    '''
