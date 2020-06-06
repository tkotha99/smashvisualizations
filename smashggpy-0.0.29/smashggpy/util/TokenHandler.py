import re

from smashggpy.util.Logger import Logger

class TokenHandler(object):

	__token = None
	__initialized = False
	__regex = re.compile('[a-f0-9]{32}')

	@staticmethod
	def init(token: str):
		log = Logger.get_instance()
		
		if not TokenHandler.__initialized:
			log.info('Checking API token: {}...'.format(token))
			if not TokenHandler.__regex.match(token):
				raise BadTokenException(token)
			elif len(token) > 32:
				raise BadTokenException(token)

			TokenHandler.__token = token
			TokenHandler.__initialized = True
			log.info('Legal API Token!')

	@staticmethod
	def get_token():
		if not TokenHandler.__initialized:
			raise NotInitializedException()
		return TokenHandler.__token

	@staticmethod
	def uninit():
		TokenHandler.__token = None
		TokenHandler.__initialized = False

from smashggpy.common.Exceptions import NotInitializedException, BadTokenException