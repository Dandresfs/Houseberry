#/usr/bin/env python
#-*- coding: utf-8 -*-
from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
import RPi.GPIO as GPIO
import time
comando = {"encender habitación principal":{"numero":[21],"estado":1,"mensaje":"Luz de la habitación principal encendida"},
	"apagar habitación principal":{"numero":[21],"estado":0,"mensaje":"Luz de la habitación principal apagada"},
           "encender baño principal":{"numero":[20],"estado":1,"mensaje":"Luz del baño principal encendida"},
           "apagar luz baño principal":{"numero":[20],"estado":0,"mensaje":"Luz del baño principal apagada"},
           "encender luz entrada":{"numero":[16],"estado":1,"mensaje":"Luz de la entrada encendida"},
           "apagar luz entrada":{"numero":[16],"estado":0,"mensaje":"Luz de la entrada apagada"},
           "encender luz sala":{"numero":[12],"estado":1,"mensaje":"Luz de la sala encendida"},
           "apagar luz sala":{"numero":[12],"estado":0,"mensaje":"Luz de la sala apagada"},
           "encender luz habitación 1":{"numero":[25,23],"estado":1,"mensaje":"Luces de la habitación 1 encendidas"},
           "apagar luz habitación 1":{"numero":[25,23],"estado":0,"mensaje":"Luces de la habitación 1 apagadas"},
           "encender baño":{"numero":[18],"estado":1,"mensaje":"Luz del baño encendida"},
           "apagar baño":{"numero":[18],"estado":0,"mensaje":"Luz del baño apagada"},
           "encender luz habitación 2":{"numero":[24],"estado":1,"mensaje":"Luz de la habitación 2 encendida"},
           "apagar luz habitación 2":{"numero":[24],"estado":0,"mensaje":"Luz de la habitación 2 apagada"},
           "encender todas":{"numero":[21,20,16,12,25,23,18,24],"estado":1,"mensaje":"Todas las luces de la casa se han encendido"},
           "apagar todas":{"numero":[21,20,16,12,25,23,18,24],"estado":0,"mensaje":"Todas las luces de la casa se han apagado"},
           }


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
	    if messageProtocolEntity.getBody().lower() == "comandos":
		comandos = "Encender/Apagar habitación principal\nEncender/Apagar baño principal\nEncender/Apagar luz entrada\nEncender/Apagar sala\nEncender/Apagar habitación 1\nEncender/Apagar baño\nEncender/Apagar habitación 2\nEncender/Apagar todas"
                print("--------------------------------------------------------------------------------")
		print("Solicitud de comandos:"+str(messageProtocolEntity.getFrom(False))+" - "+time.strftime("%I:%M:%S %p"))
                print("--------------------------------------------------------------------------------")
                self.message_send(messageProtocolEntity.getFrom(False),comandos)
                
		
            else:
		try:
			accion = comando[messageProtocolEntity.getBody().lower()]
		except:
			print("--------------------------------------------------------------------------------")
                        print("Comando inválido:"+str(messageProtocolEntity.getFrom(False))+" - "+time.strftime("%I:%M:%S %p"))
                        print("--------------------------------------------------------------------------------")
			self.message_send(messageProtocolEntity.getFrom(False),"Comando inválido")
			return
                
                for numero in accion["numero"]:
                    GPIO.output(numero,accion["estado"])
                    
		print("--------------------------------------------------------------------------------")
		print("Comando: "+str(messageProtocolEntity.getBody())+" - Numero:" +str(messageProtocolEntity.getFrom(False))+" - "+time.strftime("%I:%M:%S %p"))
                print("--------------------------------------------------------------------------------")
		self.message_send(messageProtocolEntity.getFrom(False),accion["mensaje"])
		
        else:
            print("--------------------------------------------------------------------------------")
            print("Numero no registrado:"+str(messageProtocolEntity.getFrom(False))+" - "+time.strftime("%I:%M:%S %p"))
            print("--------------------------------------------------------------------------------")
            self.message_send(messageProtocolEntity.getFrom(False),"Tu numero no esta registrado")
            

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
