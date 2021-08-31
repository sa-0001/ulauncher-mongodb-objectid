import binascii
import os
import time
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

##======================================================================================================================

def generate_objectid():
	timestamp = "{:x}".format(int(time.time()))
	rest = binascii.b2a_hex(os.urandom(8)).decode("ascii")
	return timestamp + rest

class RunExtension (Extension):
	def __init__ (self):
		super(RunExtension, self).__init__()
		self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
		self.subscribe(ItemEnterEvent, ItemEnterEventListener())

class KeywordQueryEventListener (EventListener):
	def on_event (self, event, extension):
		objectid = generate_objectid()
		items = [
			ExtensionResultItem(
				icon="images/icon.png",
				name=objectid,
				description="MongoDB ObjectId",
				highlightable=False,
				on_enter=CopyToClipboardAction(objectid),
			),
		]
		return RenderResultListAction(items)

class ItemEnterEventListener (EventListener):
	def on_event (self, event, extension):
		task_name = event.get_data() or ""
		command = extension.preferences["command"]
		command = command.replace("$TASK", task_name)
		os.system(command)
		return RenderResultListAction([])

##------------------------------------------------------------------------------

if __name__ == "__main__":
	RunExtension().run()
