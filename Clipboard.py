from PySide2 import QtGui, QtCore, QtSvg, QtWidgets, QtPrintSupport
import zipfile, io

class Clipboard():
    
    def __init__(self):
        self.clipboard = QtWidgets.QApplication.instance().clipboard()
        self.clipboard.changed.connect(self.onChanged)
        self.clipboard.dataChanged.connect(self.onDataChanged)

    def onChanged(self):
        #FreeCAD.Console.PrintMessage(s)
        print("Clipboard changed. Current mime formats: ", self.clipboard.mimeData().formats())
        print(self.getCurrentData())       

    def onDataChanged(self):
        #FreeCAD.Console.PrintMessage(s)
        print("Clipboard data changed. Current mime formats: ", self.clipboard.mimeData().formats())

    def getCurrentData(self):
        md = self.clipboard.mimeData()
        ba = md.data(md.formats()[0])
        return ba.data() 

    def getCurrentDataUnzipped(self):
        zipBytes = zipfile.ZipFile(io.BytesIO(self.getCurrentData()),"r")
        return zipBytes.read('Document.xml').decode("utf-8")

    def parseXML(self):
        data = self.getCurrentDataUnzipped()
        xml = QtCore.QXmlStreamReader(data)
        while not xml.atEnd():
            token = xml.readNext()
            if xml.isStartElement():
                print("start element ",xml.name())
            else:
                print("not start element ",xml.name())
            attr = xml.attributes()
            print("attributes count: ",len(attr))
            for a in attr:
                print(a.name()," = ",a.value())

c = Clipboard()
c.parseXML()
