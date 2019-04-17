# -*- coding: utf-8 -*-
# How to use ?
# 1. put this py file on your Maya scripts folder(e.g. maya/2018/scripts)
# 2. import this py module and run this script(e.g. import fileRenamer_en;fileRenamer_en.FileRenamerEn())

from maya import cmds
from functools import partial
from collections import OrderedDict
import pymel.core as pm
import string
import itertools

WND_NAME = 'File_Renamer'
WND_TITLE = u'File Renamer'
SEPARATOR_HIGH = 10
SEPARATOR_STYLE = 'in'
BG_COLOR_VAL = 0.741
BG_COLOR = [BG_COLOR_VAL, BG_COLOR_VAL, BG_COLOR_VAL]
WIN_POSI_X = 0
WIN_POSI_Y = 0

class FileRenamerEn(object):
    def __init__(self):
        if cmds.window(WND_NAME, ex=True):
            cmds.deleteUI(WND_NAME)
        self.win = cmds.window(WND_NAME, title=WND_TITLE, rtf=1, cc=partial(saveWindowPosition))
        self.main()
        try:
            position = [cmds.optionVar(q=WIN_POSI_X), cmds.optionVar(q=WIN_POSI_Y)]
        except ValueError:
            position = [200L, 1200L]
        cmds.window(WND_NAME, e=True, tlc=position)
        cmds.showWindow(self.win)

    def main(self):
        cmds.columnLayout(adj=1, cal='center', rs=3)
        cmds.separator(h=1, st=SEPARATOR_STYLE)
        cmds.text(l=u'Add', bgc=BG_COLOR)

        cmds.setParent('..')
        cmds.rowColumnLayout(nc=2)
        cmds.radioCollection('addNumberType')
        cmds.radioButton('add_string', l=u'Add string')
        cmds.textField('addString', tx=u'', ann=u'enter additional string', rfc=partial(selRadioButton, 'add_string'))
        cmds.radioButton('add_serial_number', l=u'Serial number：(01,02..)')
        cmds.radioButton('add_sereal_alphabet', l=u'Serial number：(AA,AB..)')
        cmds.setParent('..')
        cmds.rowColumnLayout(nr=1)
        cmds.text(l=u'　Serial number padding　')
        cmds.textField('add_paddingNumber', tx=2, ann=u'enter padding number(integer)')
        cmds.setParent('..')

        cmds.columnLayout(adj=1, cal='center', rs=3)
        cmds.separator(h=SEPARATOR_HIGH, st=SEPARATOR_STYLE)
        cmds.setParent('..')

        cmds.rowColumnLayout(nc=2)
        cmds.radioCollection('addType')
        cmds.radioButton('top', l=u'Add to lead    ')
        cmds.radioButton('bottom', l=u'Add to end')
        cmds.setParent('..')

        cmds.rowColumnLayout(nc=3)
        cmds.radioButton('topFrom', l=u'From lead to')
        cmds.textField('topFromPoint', tx=u'', rfc=partial(selRadioButton, 'topFrom'),
                       ann=u'enter number')
        cmds.text(l=u'th ')
        cmds.radioButton('bottomFrom', l=u'From end to')
        cmds.textField('bottomFromPoint', tx=u'', rfc=partial(selRadioButton, 'bottomFrom'),
                       ann=u'enter number')
        cmds.text(l=u'th ')
        cmds.setParent('..')

        cmds.columnLayout(adj=1, cal='center', rs=3)
        cmds.button(l=u'Execute addition', c=partial(addString))

        cmds.separator(h=SEPARATOR_HIGH, st=SEPARATOR_STYLE)

        cmds.text(l=u'Delete', bgc=BG_COLOR)
        cmds.rowColumnLayout(nc=3)
        cmds.radioCollection('removeType')
        cmds.radioButton('removeSpecific', l=u'String')
        cmds.textField('removeString', tx=u'', rfc=partial(selRadioButton, 'removeSpecific'),
                       ann=u'enter string to delete　e.g.：pSphere')
        cmds.text(l=u'')
        cmds.radioButton('removeTopFrom', l=u'From lead to')
        cmds.textField('removeTopFromPoint', tx=u'', rfc=partial(selRadioButton, 'removeTopFrom'),
                       ann=u'number')
        cmds.text(l=u'th ')
        cmds.radioButton('removeBottomFrom', l=u'From end to')
        cmds.textField('removeBottomFromPoint', tx=u'', rfc=partial(selRadioButton, 'removeBottomFrom'),
                       ann=u'number')
        cmds.text(l=u'th ')
        cmds.setParent('..')

        cmds.button(l=u'Execute deletion', c=partial(removeString))
        cmds.separator(h=SEPARATOR_HIGH, st=SEPARATOR_STYLE)
        cmds.button(l=u'Delete name space', c=partial(deleteNamespaece))

        cmds.separator(h=SEPARATOR_HIGH, st=SEPARATOR_STYLE)

        cmds.text(l=u'Replace', bgc=BG_COLOR)
        cmds.setParent('..')
        cmds.rowColumnLayout(nr=1)
        cmds.textField('targetString', tx=u'')
        cmds.text(l=u'　is replaced by　')
        cmds.textField('replaceString', tx=u'')
        cmds.text(l=u'　　')
        cmds.setParent('..')
        cmds.columnLayout(adj=1, cal='center', rs=3)
        cmds.button(l=u'Execute replacement', c=partial(replaceString))

        cmds.separator(h=SEPARATOR_HIGH, st=SEPARATOR_STYLE)

        cmds.text(l=u'New', bgc=BG_COLOR)
        cmds.setParent('..')
        cmds.rowColumnLayout(nr=1)
        cmds.text(l=u'　New name　')
        cmds.textField('newNameString', tx=u'', ann=u'enter new name you want')
        cmds.setParent('..')

        cmds.rowColumnLayout(nr=1)
        cmds.radioCollection('numberType')
        cmds.radioButton('serial_number', l=u'Serial number：(01,02..)')
        cmds.radioButton('sereal_alphabet', l=u'Serial number：(AA,AB..)')
        cmds.setParent('..')
        cmds.rowColumnLayout(nr=1)
        cmds.text(l=u'　Serial number padding　')
        cmds.textField('paddingNumber', tx=2, ann=u'enter padding number(integer)')
        cmds.setParent('..')
        cmds.columnLayout(adj=1, cal='center', rs=3)
        cmds.button(l=u'Execute new name', ann=u'', c=partial(setNewName))

        cmds.separator(h=SEPARATOR_HIGH, st=SEPARATOR_STYLE)

        cmds.text(l=u'')
        cmds.text(l=u'**Notice** Only selected objects are subject to processing')
        cmds.setParent('..')


def selCheck():
    sel = pm.selected()
    if not sel:
        cmds.warning(u'Select objects and execute')
        return


def selRadioButton(name, *args):
    cmds.radioButton(name, e=True, select=True)


def deleteNamespaece(*args):
    selCheck()
    before_list = OrderedDict()
    sel = cmds.ls(sl=True)
    for i in sel:
        if ':' in i:
            new_name = i.split(':')
            before_list[i] = new_name[-1]
    if before_list:
        checkWindow(before_list)


def addString(*args):
    selCheck()
    add_name = cmds.textField('addString', q=True, tx=True)
    add_type = cmds.radioCollection('addNumberType', q=True, select=True)
    add_place = cmds.radioCollection('addType', q=True, select=True)
    padding_num = cmds.textField('add_paddingNumber', q=True, tx=True)
    sel = cmds.ls(sl=True)
    num_count = 1
    alpha_count = 0
    return_list = []
    before_list = OrderedDict()
    print add_place
    if add_place == 'NONE':
        cmds.warning(u'Please select the place to add letters from the radio button(e.g.：)')
        return

    if add_type == 'add_sereal_alphabet':
        abc_list = list(string.ascii_uppercase)  #Get uppercase alphabet list
        alphabet_list = itertools.product(abc_list, repeat=int(padding_num))  #Set padding
        for i in alphabet_list:
            return_list.append(''.join(i))
            if len(return_list) > len(sel):
                break

    for i in sel:
        if add_type == 'add_serial_number':
            tmp_number = '{0:0' + str(padding_num) + 'd}'
            add_name = tmp_number.format(num_count)

        elif add_type == 'add_sereal_alphabet':
            add_name = str(return_list[alpha_count])

        if add_place == 'top':
            before_list[i] = add_name + i

        elif add_place == 'bottom':
            before_list[i] = i + add_name

        elif add_place == 'topFrom':
            split_point = cmds.textField('topFromPoint', q=True, tx=True)
            front_string = i[:int(split_point)]
            back_string = i[int(split_point):]
            before_list[i] = front_string + add_name + back_string

        elif add_place == 'bottomFrom':
            split_point = cmds.textField('bottomFromPoint', q=True, tx=True)
            front_string = i[:int(split_point)*-1]
            back_string = i[int(split_point)*-1:]
            before_list[i] = front_string + add_name + back_string

    if before_list:
        checkWindow(before_list)
    else:
        cmds.warning(u'cannot find object')


def removeString(*args):
    selCheck()
    remove_name = cmds.textField('removeString', q=True, tx=True)
    flag = cmds.radioCollection('removeType', q=True, select=True)
    before_list = OrderedDict()
    sel = cmds.ls(sl=True)
    for i in sel:
        if flag == 'removeSpecific':
            if remove_name in i:
                tmp_name = i
                new_name = tmp_name.replace(remove_name, '')
                before_list[i] = new_name

        elif flag == 'removeTopFrom':
            split_point = cmds.textField('removeTopFromPoint', q=True, tx=True)
            tmp_name = i
            new_name = tmp_name[int(split_point):]
            before_list[i] = new_name
        elif flag == 'removeBottomFrom':
            split_point = cmds.textField('removeBottomFromPoint', q=True, tx=True)
            tmp_name = i
            new_name = tmp_name[:int(split_point)*-1]
            before_list[i] = new_name

    if before_list:
        checkWindow(before_list)


def replaceString(*args):
    selCheck()
    target_name = cmds.textField('targetString', q=True, tx=True)
    replace_name = cmds.textField('replaceString', q=True, tx=True)
    sel = cmds.ls(sl=True)
    before_list = OrderedDict()
    for i in sel:
        if target_name in i:
            tmp_name = i
            new_name = tmp_name.replace(target_name, replace_name)
            before_list[i] = new_name

    if before_list:
        checkWindow(before_list)


def setNewName(*args):
    selCheck()
    sel = cmds.ls(sl=True)
    tmp_name = cmds.textField('newNameString', q=True, tx=True)
    padding_num = cmds.textField('paddingNumber', q=True, tx=True)
    number_type = cmds.radioCollection('numberType', q=True, select=True)
    num_count = 1
    alpha_count = 0
    returnList = []
    before_list = OrderedDict()

    if number_type == 'sereal_alphabet':
        abc_list = list(string.ascii_uppercase)
        alphabet_list = itertools.product(abc_list, repeat=int(padding_num))
        for i in alphabet_list:
            returnList.append(''.join(i))
            if len(returnList) > len(sel):
                break

    for i in sel:
        if number_type == 'serial_number':
            tmp_number = '{0:0'+str(padding_num)+'d}'
            number = tmp_number.format(num_count)
            new_name = tmp_name + str(number)
            before_list[i] = new_name
            num_count += 1
        elif number_type == 'sereal_alphabet':
            new_name = tmp_name + str(returnList[alpha_count])
            before_list[i] = new_name
            alpha_count += 1

    if before_list:
        checkWindow(before_list)


def returnAlphabetList(count, padding, *args):
    abc_list = list(string.ascii_uppercase)
    alphabet_list = itertools.product(abc_list, repeat=int(padding))
    returnList = []
    for i in alphabet_list:
        returnList.append(''.join(i))
    return returnList[count]


def checkWindow(before_list, *args):
    text_width = 250
    if cmds.window('check_window', ex=1):
        cmds.deleteUI('check_window', window=True)
    cmds.window('check_window', title=u'Confirm rename')

    cmds.columnLayout(adj=True, cal='center', rs=3)
    cmds.separator(h=SEPARATOR_HIGH, st=SEPARATOR_STYLE)

    root = cmds.rowColumnLayout('check_root', nc=2)
    before = cmds.frameLayout('check_before', l=u'Before', p=root, w=text_width, bv=True, lv=False)
    cmds.textScrollList('before', p=before, h=300)
    for i in before_list.keys():
        cmds.textScrollList('before', e=True, a=i)
    after = cmds.frameLayout('check_after', l=u'After', p=root, w=text_width, bv=True, lv=False)
    cmds.textScrollList('after', p=after, h=300)
    for i in before_list.values():
        cmds.textScrollList('after', e=True, a=i)
    cmds.setParent('..')
    cmds.setParent('..')

    cmds.columnLayout(adj=True, cal='center', rs=3)
    cmds.separator(h=SEPARATOR_HIGH, st=SEPARATOR_STYLE)
    cmds.button(l='Execute', w=text_width*2, c=partial(runRename, before_list))
    cmds.separator(h=SEPARATOR_HIGH, st=SEPARATOR_STYLE)
    cmds.setParent('..')

    cmds.showWindow('check_window')


def runRename(before_list, *args):
    for key, val in before_list.items():
        cmds.rename(key, val)

    if cmds.window('check_window', ex=1):
        cmds.deleteUI('check_window', window=True)


def saveWindowPosition():
    val = cmds.window(WND_NAME, q=True, tlc=True)
    cmds.optionVar(iv=(WIN_POSI_X, val[0]))
    cmds.optionVar(iv=(WIN_POSI_Y, val[1]))

