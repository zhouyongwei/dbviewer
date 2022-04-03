#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    分页支持类
"""


class Pager(object):
    def __init__(self, totalRows, perPageRows):
        self.totalRows = totalRows
        self.perPageRows = perPageRows
        self.begRow = 0
        if self.totalRows < self.perPageRows:
            self.endRow = self.totalRows
        else:
            self.endRow = self.perPageRows

    def up(self):
        if not self.begRow:
            pass
        else:
            self.endRow = self.begRow
            self.begRow -= self.perPageRows
        return self.begRow, self.endRow

    def down(self):
        if self.endRow >= self.totalRows:
            pass
        elif self.endRow + self.perPageRows > self.totalRows:
            self.begRow = self.endRow
            self.endRow = self.totalRows
        else:
            self.begRow = self.endRow
            self.endRow += self.perPageRows
        return self.begRow, self.endRow


if __name__ == '__main__':
    pager = Pager(48, 9)
    print(pager.up())
    print(pager.up())
    print(pager.up())
    print(pager.down())
    print(pager.down())
    print(pager.down())
    print(pager.down())
    print(pager.down())
    print(pager.down())
    print(pager.down())
    print(pager.down())
    print(pager.down())
    print(pager.down())
    print(pager.down())
    print(pager.up())
