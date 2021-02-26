"""
Combo box with auto complete (Completer). It's not really working though.
"""
import json
import logging
from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork

LOG = logging.getLogger(__name__)

class SuggestionPlaceModel(QtGui.QStandardItemModel):
    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(SuggestionPlaceModel, self).__init__(parent)
        self._manager = QtNetwork.QNetworkAccessManager(self)
        self._reply = None

    @QtCore.pyqtSlot(str)
    def search(self, text):
        self.clear()
        if self._reply is not None:
            self._reply.abort()
        if text:
            r = self.create_request(text)
            self._reply = self._manager.get(r)
            self._reply.finished.connect(self.on_finished)
        loop = QtCore.QEventLoop()
        self.finished.connect(loop.quit)
        loop.exec_()

    def create_request(self, text):
        url = QtCore.QUrl("https://api3.geo.admin.ch/rest/services/api/SearchServer")
        query = QtCore.QUrlQuery()
        query.addQueryItem("sr", "2056")
        query.addQueryItem("searchText", text)
        query.addQueryItem("lang", "en")
        query.addQueryItem("type", "locations")
        url.setQuery(query)
        request = QtNetwork.QNetworkRequest(url)
        return request

    @QtCore.pyqtSlot()
    def on_finished(self):
        reply = self.sender()
        if reply.error() == QtNetwork.QNetworkReply.NoError:
            data = json.loads(reply.readAll().data())
            # LOG.debug(data)
            if data.get('status') != 'error':
                for location in data['results']:
                    label = location.get('attrs', {}).get('label', 'Unknown label')
                    self.appendRow(QtGui.QStandardItem(label))
                    # LOG.debug(label + str(self.rowCount()))
            else:
                self.error.emit(data.get('detail', 'Unknown error detail'))
        self.finished.emit()
        reply.deleteLater()
        self._reply = None

class Completer(QtWidgets.QCompleter):
    def splitPath(self, path):
        self.model().search(path)
        return super(Completer, self).splitPath(path)

class AutoWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        LOG.debug('1')
        super(Widget, self).__init__(parent)
        LOG.debug('2')
        self._model = SuggestionPlaceModel(self)
        LOG.debug('3')
        completer = Completer(self, caseSensitivity=QtCore.Qt.CaseInsensitive)
        LOG.debug('4')
        completer.setModel(self._model)
        LOG.debug('5')
        lineedit = QtWidgets.QLineEdit()
        LOG.debug('6')
        lineedit.setCompleter(completer)
        LOG.debug('7')
        label = QtWidgets.QLabel()
        LOG.debug('8')
        self._model.error.connect(label.setText)
        LOG.debug('9')
        lay = QtWidgets.QFormLayout(self)
        LOG.debug('10')
        lay.addRow("Location: ", lineedit)
        LOG.debug('11')
        lay.addRow("Error: ", label)
        LOG.debug('12')
