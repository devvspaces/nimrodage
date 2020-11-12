from django.conf import settings
import hashlib
import random
import string

salt = settings.SECRET_KEY
def generation(challenge=salt, size = 25):
	answer = ''.join(random.choice(string.ascii_lowercase +
		string.ascii_uppercase +
		string.digits) for x in range(size))
	
	attempt = challenge+answer

	return attempt, answer

sha = hashlib.sha256()


def makeCode():
	attempt, answer = generation()
	sha.update(attempt.encode())
	return sha.hexdigest()

def encrypt_string(hash_string):
    sha_signature = hashlib.md5(hash_string.encode()).hexdigest()
    return sha_signature


def random_str_gen(size, chars=string.ascii_lowercase+string.digits):
	return ''.join([random.choice(chars) for _ in  range(size)])

def create_slug(instance, new_slug=None):
	#create slug
	if new_slug:
		tid=slugify(new_slug)
	else:
		tid=encrypt_string(random_str_gen(5))
	klass=instance.__class__
	#if tid already exist
	qs_exists=klass.objects.filter(tid=tid).exists()
	if qs_exists:
		new_tid=encrypt_string(random_str_gen(5))
		return create_slug(instance, new_tid)
	return tid