from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction

import utils
import logging

converter = utils.CurrencyConv()      # one global converter
logger = logging.getLogger(__name__)

class CurrencyConvExtension(Extension):
    def __init__(self):
        super(CurrencyConvExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        logger.info('cu get event')
        args = event.get_argument()
        items = []

        if args == None:
            items.append(ExtensionResultItem(icon='images/icon.png',
                                            name='input format: {number} {type}',
                                            description='enter to see all the format',
                                            on_enter=ExtensionCustomAction('help', True)))
            return RenderResultListAction(items)

        try:
            val, src_type, dst_type = converter.parse(args)
            result = converter.convert(src_type, dst_type, val)
            des = 'Enter to copy the number to the clipboard'
            items.append(ExtensionResultItem(icon='images/icon.png',
                                            name='{} {}'.format(result, dst_type),
                                            description=des,
                                            on_enter=CopyToClipboardAction(str(result))))
        except utils.syntaxError as e:
            items.append(ExtensionResultItem(icon='images/icon.png',
                                            name='syntax error',
                                            description='enter to open the help menu',
                                            on_enter=ExtensionCustomAction('help', True)))
        except utils.typeNotFoundError as e:
            items.append(ExtensionResultItem(icon='images/icon.png',
                                            name='Can\'t recognize the currency: "{}" '.format(e.args[0]),
                                            description='',
                                            on_enter=HideWindowAction()))

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        cmd = event.get_data()
        items = []
        if cmd == 'help':
            items.append(ExtensionResultItem(name='{number} {source type}',
                                            on_enter=HideWindowAction()))
            items.append(ExtensionResultItem(name='{number} {source type} {target type}',
                                            on_enter=HideWindowAction()))
            items.append(ExtensionResultItem(name='{number} {source type} to {target type}',
                                            on_enter=HideWindowAction()))
        else:
            items.append(ExtensionResultItem(name='sub page not found...',
                                            on_enter=HideWindowAction()))
        return RenderResultListAction(items)

if __name__ == '__main__':
    CurrencyConvExtension().run()
