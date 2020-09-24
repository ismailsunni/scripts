"""
A script to show that a python object is deleted although it's still referenced. Only occurs in Kadas's Python.

Also example for using QCompleter with list from URL response. Not really works though.

@ismailsunni / imajimatika@gmail.com - Sept 2020
"""

import json

from PyQt5.QtCore import Qt, pyqtSignal, QEventLoop, pyqtSlot, QUrl, QUrlQuery
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtWidgets import QCompleter, QLineEdit, QLabel, QFormLayout, QApplication, QWidget, QCheckBox

class SuggestionPlaceModel(QStandardItemModel):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SuggestionPlaceModel, self).__init__(parent)
        self._manager = QNetworkAccessManager(self)
        self._reply = None

    @pyqtSlot(str)
    def search(self, text):
        self.clear()
        if self._reply is not None:
            self._reply.abort()
        if text:
            r = self.create_request(text)
            print(r.url().toString())
            self._reply = self._manager.get(r)
            self._reply.finished.connect(self.on_finished)
        loop = QEventLoop()
        self.finished.connect(loop.quit)
        loop.exec_()

    def create_request(self, text):
        url = QUrl("https://api3.geo.admin.ch/rest/services/api/SearchServer")
        query = QUrlQuery()
        query.addQueryItem("sr", "2056")
        query.addQueryItem("searchText", text)
        query.addQueryItem("lang", "en")
        query.addQueryItem("type", "locations")
        query.addQueryItem("limit", "10")
        url.setQuery(query)
        request = QNetworkRequest(url)
        return request

    @pyqtSlot()
    def on_finished(self):
        reply = self.sender()
        if reply.error() == QNetworkReply.NoError:
            data = json.loads(reply.readAll().data())
            if data.get('status') != 'error':
                print(data['results'])
                for location in data['results']:
                    attributes = location.get('attrs', {})
                    label = attributes.get('label', 'Unknown label')
                    print(label)
                    self.appendRow(QStandardItem(label))
            self.error.emit(data.get('detail', 'Unknown error detail'))
        self.finished.emit()
        reply.deleteLater()
        self._reply = None

class Completer(QCompleter):
    def splitPath(self, path):
        print('split path for %s' % path)
        self.model().search(path)
        return super(Completer, self).splitPath(path)

class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self._model = SuggestionPlaceModel(self)
        self._completer = Completer(self, caseSensitivity=Qt.CaseInsensitive)
        self._completer.setModel(self._model)
        self._lineedit = QLineEdit()
        self._lineedit.setCompleter(self._completer)
        self._label = QLabel()
        self._model.error.connect(self._label.setText)
        # check box
        self._cbx = QCheckBox()
        self._cbx.setChecked(True)
        self._cbx.toggled.connect(self.enableAutoComplete)
        lay = QFormLayout(self)
        lay.addRow("Location: ", self._lineedit)
        lay.addRow("Error: ", self._label)
        lay.addRow("Enable", self._cbx)

    def enableAutoComplete(self, state):
        if state:
            print('Auto complete is enabled')
            self._lineedit.setCompleter(self._completer)
        else:
            print('Auto complete is disabled')
            self._lineedit.setCompleter(None)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = Widget()
    w.resize(400, w.sizeHint().height())
    w.show()
    sys.exit(app.exec_())
