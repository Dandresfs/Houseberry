from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity

class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        if messageProtocolEntity.getType() == 'text':
            self.onTextMessage(messageProtocolEntity)
        elif messageProtocolEntity.getType() == 'media':
            self.onMediaMessage(messageProtocolEntity)

        self.toLower(messageProtocolEntity.ack(True))




    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    def onTextMessage(self,messageProtocolEntity):
        # just print info
        archivo = open('numeros')
        numeros = archivo.readlines()
        numeros = [numero.replace('\n', '') for numero in numeros]
        if len(filter(lambda x: str(messageProtocolEntity.getFrom(False)) in x, numeros)) > 0:
            self.message_send(messageProtocolEntity.getFrom(False),"Estas registrado pero ahorita no joven")
        else:
            self.message_send(messageProtocolEntity.getFrom(False),"Tu numero no esta registrado")
        print("Echoing %s to %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))

    def onMediaMessage(self, messageProtocolEntity):
        # just print info
        if messageProtocolEntity.getMediaType() == "image":
            print("Echoing image %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.getMediaType() == "location":
            print("Echoing location (%s, %s) to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.getMediaType() == "vcard":
            print("Echoing vcard (%s, %s) to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))

    def message_send(self, number, content):
        outgoingMessage = TextMessageProtocolEntity(content, to=self.normalizeJid(number))
        self.toLower(outgoingMessage)

    def normalizeJid(self, number):
        if '@' in number:
            return number

        return "%s@s.whatsapp.net" % number