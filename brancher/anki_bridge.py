# -*- coding: utf-8 -*-

# Copyright (C) 2013  Alex Yatskov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sys

from aqt import mw
from aqt.qt import *
import aqt
from aqt.utils import showInfo
import anki
import anki.collection
from anki.hooks import addHook
from anki.hooks import runFilter
from anki.sched import Scheduler
from anki.models import defaultModel,defaultField,defaultTemplate
from brancher import *

from goo import Goo
from tatoeba import Tatoeba
from treelib import Node, Tree

class Anki:
    def createBrancherModel(self):
        models = self.collection().models
        if u'BrancherJapanese' not in models.allNames():
            model = models.new(u'BrancherJapanese')
            model['css'] = """\
.card {
 font-family: arial;
 font-size: 22px;
 text-align: center;
 color: black;
 background-color: white;
}

.card1 { background-color: #ffff7f; }
.card2 { background-color: #efff7f; }
            """
            for field in [u'Expression',u'Definition',u'Keyword',u'Reading']:
                models.addField(model,models.newField(field))
            template = models.newTemplate(u'Production')
            template['qfmt'] = u'{{Expression}}'
            template['afmt'] = u'{{furigana:Reading}}<hr>{{Keyword}}:{{Definition}}'
            models.addTemplate(model,template)
            models.add(model)
            models.flush()
        decks = self.collection().decks
        if u'Brancher' not in decks.allNames():
            decks.id(u'Brancher')

    def addNote(self, deckName, modelName, fields, tags=list()):
        note = self.createNote(deckName, modelName, fields, tags)
        if note is not None:
            self.startEditing()
            collection = self.collection()
            collection.addNote(note)
            collection.autosave()
            srcIdx = 0
            for c, name in enumerate(mw.col.models.fieldNames(note.model())):
                if name == 'Expression':
                    srcIdx = c
            runFilter("editFocusLost", False, note, srcIdx)#note.fields.index('Expression'))
            self.stopEditing()
            return note.id

    def canAddNote(self, deckName, modelName, fields):
        return bool(self.createNote(deckName, modelName, fields))

    def createNote(self, deckName, modelName, fields, tags=list()):
        model = self.models().byName(modelName)
        if model is None:
            return None

        deck = self.decks().byName(deckName)
        if deck is None:
            return None

        note = anki.notes.Note(self.collection(), model)
        note.model()['did'] = deck['id']
        note.tags = tags

        for name, value in fields.items():
            if name in note:
                note[name] = value

        if not note.dupeOrEmpty():
            return note

    def browse(self, query):
        browser = aqt.dialogs.open('Browser', self.window())
        browser.form.searchEdit.lineEdit().setText(u' '.join([u'{0}:{1}'.format(key,value) for key,value in query.items()]))
        browser.onSearch()

    def getNotes(self, modelName, key, value):
        return self.collection().findNotes(key + u':' + value + u' note:' + modelName)

    def getCards(self, modelName, onlyFirst = False):
        model = self.models().byName(modelName)
        modelid = int(model[u"id"])
        query = "select " + ("min(c.id)" if onlyFirst else "c.id")
        query+= ",n.sfld,n.id from cards c "
        query+= "join notes n on (c.nid = n.id) " 
        query+= "where n.mid=%d" % (modelid)
        if onlyFirst: query+= "group by n.id"
        return self.collection().db.execute(query)

    def getCardsByNote(self, modelName, key, value):
        return self.collection().findCards(key + u':' + value + u' note:' + modelName)

    def getCardsByNoteAndNotInDeck(self, modelName, values, did):
        model = self.models().byName(modelName)
        modelid = int(model[u"id"])
        query = u"select c.id from cards c "
        query+= u"join notes n on (c.nid = n.id) " 
        query+= u"where n.mid=%d " % (modelid)
        query+= u"and c.did!=%d " % (did)
        query+= u"and n.sfld in " + (u"(%s)" % u",".join([u"'%s'"%(s) for s in values]))
        self.query = query
        return self.collection().db.execute(query)

    def getModelKey(self, modelName):
        model = self.collection().models.byName(modelName)
        if model is None:
            return None
        frstfld = model[u"flds"][0]
        return frstfld[u"name"]

    def startEditing(self):
        self.window().requireReset()

    def stopEditing(self):
        if self.collection():
            self.window().maybeReset()

    def window(self):
        return aqt.mw

    def addUiAction(self, action):
        self.window().form.menuTools.addAction(action)

    def collection(self):
        return self.window().col

    def models(self):
        return self.collection().models

    def modelNames(self):
        return self.models().allNames()

    def modelFieldNames(self, modelName):
        model = self.models().byName(modelName)
        if model is not None:
            return [field['name'] for field in model['flds']]

    def decks(self):
        return self.collection().decks


    def deckNames(self):
        return self.decks().allNames()

class BrancherPlugin:
    def __init__(self):
        self.anki = Anki()
        self.brancher = BrancherWidget()
        self.brancher.anki = self.anki

    def show(self):
        self.brancher.show()

brancherInstance = BrancherPlugin()

def onBeforeStateChange(state, oldState, *args):
    brancherInstance.anki.createBrancherModel()

addHook('beforeStateChange',onBeforeStateChange)
