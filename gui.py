#!/usr/bin/env python
'''
this gui based on pyqt and used the example - findfiles.pyw as template.
'''

from PyQt4 import QtCore, QtGui
import cutwhite


class Window(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        browseButton = self.createButton("&Browse...", self.browse)
        browse2Button = self.createButton("&Browse...", self.browse2)
        findButton = self.createButton("&Find PDF", self.find)
        actionButton = self.createButton("&Cut White", self.doAction)

        self.fileComboBox = self.createComboBox("*.pdf")
        self.textComboBox = self.createComboBox()
        self.directoryComboBox = self.createComboBox()#(QtCore.QDir.currentPath())
        self.directory2ComboBox = self.createComboBox()#(QtCore.QDir.currentPath())

        fileLabel = QtGui.QLabel("Named:")
        directoryLabel = QtGui.QLabel("Input directory:")
        directory2Label = QtGui.QLabel("Output directory:")
        self.filesFoundLabel = QtGui.QLabel()

        self.createFilesTable()

        buttonsLayout = QtGui.QHBoxLayout()
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(findButton)
        buttonsLayout.addWidget(actionButton)

        mainLayout = QtGui.QGridLayout()
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
        mainLayout.addLayout(buttonsLayout, 6, 0, 1, 3)
        self.setLayout(mainLayout)

        self.setWindowTitle("PDF Cut White")
        self.resize(700, 300)

    def browse(self):
        directory = QtGui.QFileDialog.getExistingDirectory(
            self, "Input Dir", QtCore.QDir.currentPath())

        if directory:
            if self.directoryComboBox.findText(directory) == -1:
                self.directoryComboBox.addItem(directory)

            self.directoryComboBox.setCurrentIndex(
                self.directoryComboBox.findText(directory))

    def browse2(self):
        directory = QtGui.QFileDialog.getExistingDirectory(
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

    def doAction(self):
        """
        do action to cut the white and output new pdf
        """
        indir = self.directoryComboBox.currentText()
        outdir = self.directory2ComboBox.currentText()

        cnt = self.filesTable.rowCount()
        for row in range(cnt):
            item = self.filesTable.item(row, 0)
            name = item.text()

            #qstring to string
            input = unicode(indir +"\\"+ name)
            output = unicode(outdir +"\\"+ name)

            cutwhite.cut_white(input, output)

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
        progressDialog = QtGui.QProgressDialog(self)

        progressDialog.setCancelButtonText("&Cancel")
        progressDialog.setRange(0, files.count())
        progressDialog.setWindowTitle("Find Files")

        foundFiles = []

        for i in range(files.count()):
            progressDialog.setValue(i)
            progressDialog.setLabelText("Searching file number %d of %d..." %
                                        (i, files.count()))
            QtGui.qApp.processEvents()

            if progressDialog.wasCanceled():
                break

            inFile = QtCore.QFile(self.currentDir.absoluteFilePath(files[i]))

        progressDialog.close()

        return foundFiles

    def showFiles(self, files):
        for fn in files:
            file = QtCore.QFile(self.currentDir.absoluteFilePath(fn))
            size = QtCore.QFileInfo(file).size()

            fileNameItem = QtGui.QTableWidgetItem(fn)
            fileNameItem.setFlags(fileNameItem.flags() ^
                                  QtCore.Qt.ItemIsEditable)
            sizeItem = QtGui.QTableWidgetItem("%d KB" %
                                              (int((size + 1023) / 1024)))
            sizeItem.setTextAlignment(QtCore.Qt.AlignVCenter |
                                      QtCore.Qt.AlignRight)
            sizeItem.setFlags(sizeItem.flags() ^ QtCore.Qt.ItemIsEditable)

            row = self.filesTable.rowCount()
            self.filesTable.insertRow(row)
            self.filesTable.setItem(row, 0, fileNameItem)
            self.filesTable.setItem(row, 1, sizeItem)

        self.filesFoundLabel.setText(
            "%d file(s) found (Double click on a file to open it)" %
            len(files))

    def createButton(self, text, member):
        button = QtGui.QPushButton(text)
        button.clicked.connect(member)
        return button

    def createComboBox(self, text=""):
        comboBox = QtGui.QComboBox()
        comboBox.setEditable(True)
        comboBox.addItem(text)
        comboBox.setSizePolicy(QtGui.QSizePolicy.Expanding,
                               QtGui.QSizePolicy.Preferred)
        return comboBox

    def createFilesTable(self):
        self.filesTable = QtGui.QTableWidget(0, 2)
        self.filesTable.setSelectionBehavior(
            QtGui.QAbstractItemView.SelectRows)

        self.filesTable.setHorizontalHeaderLabels(("File Name", "Size"))
        self.filesTable.horizontalHeader().setResizeMode(
            0, QtGui.QHeaderView.Stretch)
        self.filesTable.verticalHeader().hide()
        self.filesTable.setShowGrid(False)

        self.filesTable.cellActivated.connect(self.openFileOfItem)

    def openFileOfItem(self, row, column):
        item = self.filesTable.item(row, 0)

        QtGui.QDesktopServices.openUrl(QtCore.QUrl(
            self.currentDir.absoluteFilePath(item.text())))


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
