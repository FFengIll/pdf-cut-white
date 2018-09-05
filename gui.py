#!/usr/bin/env python
# encoding=utf-8
'''
this gui based on PySide2 (QT for Python) and used the example - findfiles.pyw as template.
'''

import sys
import os
import traceback

from PySide2 import QtWidgets, QtCore, QtWidgets

import cutwhite


class Window(QtWidgets.QDialog):
    def __init__(self):
        super(Window, self).__init__()

        browseButton = self.createButton("&Browse...", self.browseInDir)
        browse2Button = self.createButton("&Browse...", self.browseOutDir)
        findButton = self.createButton("&Find PDF", self.find)
        actionButton = self.createButton("&Cut White", self.doAction)
        allButton = self.createButton("&Select All", self.selectAll)
        unallButton = self.createButton("&Unselect All", self.unselectAll)

        self.fileComboBox = self.createComboBox("*.pdf")
        self.textComboBox = self.createComboBox()
        self.directoryComboBox = self.createComboBox(QtCore.QDir.currentPath())
        self.directory2ComboBox = self.createComboBox(
            os.path.join(QtCore.QDir.currentPath(), 'output'))

        fileLabel = QtWidgets.QLabel("Named:")
        directoryLabel = QtWidgets.QLabel("Input directory:")
        directory2Label = QtWidgets.QLabel("Output directory:")
        self.filesFoundLabel = QtWidgets.QLabel()

        self.createFilesTable()

        buttonsLayout = QtWidgets.QHBoxLayout()
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(findButton)
        buttonsLayout.addWidget(actionButton)

        checkButtonLayout = QtWidgets.QHBoxLayout()
        checkButtonLayout.addStretch()
        checkButtonLayout.addWidget(allButton)
        checkButtonLayout.addWidget(unallButton)

        mainLayout = QtWidgets.QGridLayout()
        mainLayout.addWidget(fileLabel, 0, 0)
        mainLayout.addWidget(self.fileComboBox, 0, 1, 1, 2)

        mainLayout.addWidget(directoryLabel, 2, 0)
        mainLayout.addWidget(self.directoryComboBox, 2, 1)
        mainLayout.addWidget(browseButton, 2, 2)

        mainLayout.addWidget(directory2Label, 3, 0)
        mainLayout.addWidget(self.directory2ComboBox, 3, 1)
        mainLayout.addWidget(browse2Button, 3, 2)

        mainLayout.addWidget(self.filesTable, 4, 0, 1, 3)
        mainLayout.addWidget(self.filesFoundLabel, 5, 0, 1, 3)
        mainLayout.addLayout(checkButtonLayout, 6, 0)
        mainLayout.addLayout(buttonsLayout, 6, 1, 1, 2)
        self.setLayout(mainLayout)

        self.setWindowTitle("PDF Cut White")
        self.resize(700, 500)

    def browseInDir(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Input Dir", QtCore.QDir.currentPath())

        if directory:
            if self.directoryComboBox.findText(directory) == -1:
                self.directoryComboBox.addItem(directory)

            self.directoryComboBox.setCurrentIndex(
                self.directoryComboBox.findText(directory))

    def browseOutDir(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Output Dir", QtCore.QDir.currentPath())

        if directory:
            if self.directory2ComboBox.findText(directory) == -1:
                self.directory2ComboBox.addItem(directory)

            self.directory2ComboBox.setCurrentIndex(
                self.directory2ComboBox.findText(directory))

    @staticmethod
    def updateComboBox(comboBox):
        if comboBox.findText(comboBox.currentText()) == -1:
            comboBox.addItem(comboBox.currentText())

    def setCheck(self, flag):
        cnt = self.filesTable.rowCount()
        for row in range(cnt):
            checkitem = self.filesTable.item(row, 0)
            if checkitem.checkState() == QtCore.Qt.Unchecked:
                checkitem.setCheckState(flag)

    def selectAll(self):
        self.setCheck(QtCore.Qt.Checked)

    def unselectAll(self):
        self.setCheck(QtCore.Qt.UnChecked)

    def doAction(self):
        """
        do action to cut the white and output new pdf
        """
        indir = self.directoryComboBox.currentText()
        outdir = self.directory2ComboBox.currentText()

        success = True
        msg = ""
        cnt = self.filesTable.rowCount()
        for row in range(cnt):
            checkitem = self.filesTable.item(row, 0)
            if checkitem.checkState() == QtCore.Qt.Unchecked:
                continue
            item = self.filesTable.item(row, 1)
            name = item.text()

            # qstring to string
            input = os.path.join(indir, name)
            output = os.path.join(outdir, name)

            try:
                cutwhite.cut_white(str(input), str(output))
            except Exception as e:
                print("error while cut white")
                traceback.print_exc()
                msg = traceback.format_exc()
                success = False
                break
        if(success):
            QtWidgets.QMessageBox.information(
                self, "Info", "Completed!", QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.warning(
                self, "Error", "Error while process: \n%s" % (msg), QtWidgets.QMessageBox.Ok)

        # cutwhite.batch_action(indir,outdir)

    def find(self):
        self.filesTable.setRowCount(0)

        fileName = self.fileComboBox.currentText()
        text = self.textComboBox.currentText()
        path = self.directoryComboBox.currentText()

        self.updateComboBox(self.fileComboBox)
        self.updateComboBox(self.textComboBox)
        self.updateComboBox(self.directoryComboBox)

        self.currentDir = QtCore.QDir(path)
        if not fileName:
            fileName = "*"
        files = self.currentDir.entryList(
            [fileName], QtCore.QDir.Files | QtCore.QDir.NoSymLinks)

        if text:
            files = self.findFiles(files, text)
        self.showFiles(files)

    def findFiles(self, files, text):
        progressDialog = QtWidgets.QProgressDialog(self)

        progressDialog.setCancelButtonText("&Cancel")
        progressDialog.setRange(0, files.count())
        progressDialog.setWindowTitle("Find Files")

        foundFiles = []

        for i in range(files.count()):
            progressDialog.setValue(i)
            progressDialog.setLabelText("Searching file number %d of %d..." %
                                        (i, files.count()))
            QtWidgets.qApp.processEvents()

            if progressDialog.wasCanceled():
                break

            inFile = QtCore.QFile(self.currentDir.absoluteFilePath(files[i]))

        progressDialog.close()

        return foundFiles

    def showFiles(self, files):
        for fn in files:
            file = QtCore.QFile(self.currentDir.absoluteFilePath(fn))
            size = QtCore.QFileInfo(file).size()

            fileNameItem = QtWidgets.QTableWidgetItem(fn)
            fileNameItem.setFlags(fileNameItem.flags() ^
                                  QtCore.Qt.ItemIsEditable)
            sizeItem = QtWidgets.QTableWidgetItem("%d KB" %
                                                  (int((size + 1023) / 1024)))
            sizeItem.setTextAlignment(QtCore.Qt.AlignVCenter |
                                      QtCore.Qt.AlignRight)
            sizeItem.setFlags(sizeItem.flags() ^ QtCore.Qt.ItemIsEditable)

            # a check item to choose the spec files
            checkItem = QtWidgets.QTableWidgetItem()
            checkItem.setCheckState(QtCore.Qt.Checked)
            checkItem.setTextAlignment(QtCore.Qt.AlignVCenter |
                                       QtCore.Qt.AlignHCenter)

            row = self.filesTable.rowCount()
            self.filesTable.insertRow(row)
            self.filesTable.setItem(row, 0, checkItem)
            self.filesTable.setItem(row, 1, fileNameItem)
            self.filesTable.setItem(row, 2, sizeItem)

        self.filesFoundLabel.setText(
            "%d file(s) found (Double click on a file to open it)" %
            len(files))

    def createButton(self, text, member):
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(member)
        return button

    def createComboBox(self, text=""):
        comboBox = QtWidgets.QComboBox()
        comboBox.setEditable(True)
        comboBox.addItem(text)
        comboBox.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                               QtWidgets.QSizePolicy.Preferred)
        return comboBox

    def createFilesTable(self):
        self.filesTable = QtWidgets.QTableWidget(0, 3)
        self.filesTable.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)

        self.filesTable.setHorizontalHeaderLabels(("Choose", "File Name",
                                                   "Size"))
        # self.filesTable.horizontalHeader().setResizeMode(
        #     1, QtWidgets.QHeaderView.Stretch)
        self.filesTable.verticalHeader().hide()
        self.filesTable.setShowGrid(False)

        self.filesTable.cellActivated.connect(self.openFileOfItem)

    def openFileOfItem(self, row, column):
        item = self.filesTable.item(row, 0)

        QtWidgets.QDesktopServices.openUrl(QtCore.QUrl(
            self.currentDir.absoluteFilePath(item.text())))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
