#Required pip libraries: boto3, playsound
#Author: Cole Bianchi, Amazon AWS

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
import playsound

session = Session(profile_name='default')
polly = session.client('polly', region_name='us-east-2')

def play(text):
	print("Sending tts request to AWS with text: "+text)

	try:
		response = polly.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Brian')

		if 'AudioStream' in response:

			with closing(response['AudioStream']) as stream:
				output = os.path.join(gettempdir(), 'last_tts.mp3')

				try:
					with open(output, 'wb') as file:
						file.write(stream.read())

					playsound.playsound(output, True)
				except IOError:
					print("ERROR: IOError")
					return "IOERROR"

	except ClientError:
		print("ERROR: ClientError")
		return "CLIENTERROR"
	except BotoCoreError:
		print("ERROR: BotoCoreError")
		return "BOTOCOREERROR"
