from yowsup.stacks import YowStack
from layer import EchoLayer
from yowsup.layers import YowLayerEvent
from yowsup.layers.auth                        import YowCryptLayer, YowAuthenticationProtocolLayer, AuthError
from yowsup.layers.coder                       import YowCoderLayer
from yowsup.layers.network                     import YowNetworkLayer
from yowsup.layers.protocol_messages           import YowMessagesProtocolLayer
from yowsup.layers.protocol_media              import YowMediaProtocolLayer
from yowsup.layers.stanzaregulator             import YowStanzaRegulator
from yowsup.layers.protocol_receipts           import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks               import YowAckProtocolLayer
from yowsup.layers.logger                      import YowLoggerLayer
from yowsup.layers.protocol_iq                 import YowIqProtocolLayer
from yowsup.layers.protocol_calls              import YowCallsProtocolLayer
from yowsup.common import YowConstants
from yowsup import env
import logging
import RPi.GPIO as GPIO

class YowsupEchoStack(object):
    def __init__(self, credentials, encryptionEnabled = False):
	GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
	GPIO.setup(21, GPIO.OUT)	#Led 1
	GPIO.setup(20, GPIO.OUT)	#Led 2
	GPIO.setup(16, GPIO.OUT)        #Led 3
	GPIO.setup(12, GPIO.OUT)        #Led 4
	GPIO.setup(25, GPIO.OUT)        #Led 5
	GPIO.setup(24, GPIO.OUT)        #Led 6
	GPIO.setup(23, GPIO.OUT)        #Led 7
	GPIO.setup(18, GPIO.OUT)        #Led 8
        GPIO.setup(19, GPIO.OUT)
        GPIO.setup(26, GPIO.OUT)
        entrada = GPIO.PWM(19,50)
        entrada.start(12)
        garaje = GPIO.PWM(26,50)
        garaje.start(3.5)

	GPIO.output(21, GPIO.LOW)
	GPIO.output(20, GPIO.LOW)
	GPIO.output(16, GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
	GPIO.output(25, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)
	GPIO.output(23, GPIO.LOW)
        GPIO.output(18, GPIO.LOW)

        if encryptionEnabled:
            from yowsup.layers.axolotl                     import YowAxolotlLayer
            layers = (
                EchoLayer,
                (YowAuthenticationProtocolLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer, YowMediaProtocolLayer, YowIqProtocolLayer, YowCallsProtocolLayer),
                YowAxolotlLayer,
                YowLoggerLayer,
                YowCoderLayer,
                YowCryptLayer,
                YowStanzaRegulator,
                YowNetworkLayer
            )
        else:
            layers = (
                EchoLayer,
                (YowAuthenticationProtocolLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer, YowMediaProtocolLayer, YowIqProtocolLayer, YowCallsProtocolLayer),
                YowLoggerLayer,
                YowCoderLayer,
                YowCryptLayer,
                YowStanzaRegulator,
                YowNetworkLayer
            )
        logging.basicConfig()
        self.stack = YowStack(layers)
        self.stack.setCredentials(credentials)

    def start(self):
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
	

        try:
            self.stack.loop()
        except AuthError as e:
            print("Authentication Error: %s" % e.message)
