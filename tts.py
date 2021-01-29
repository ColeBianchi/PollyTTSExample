#Required pip libraries: boto3, audioplayer
#Author: Cole Bianchi, Amazon AWS

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
import audioplayer

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

					player = audioplayer.AudioPlayer(output)
					player.play(loop=False, block=True)
					player.close()
					
				except IOError as error:
					print(error)
					return error

	except ClientError as error:
		print(error)
		return error
	except BotoCoreError as error:
		print(error)
		return error
