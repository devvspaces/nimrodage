from Home.utils import makeCode
from .models import Views

def createViewer(new_hash=None):
	#create unique code
	if new_hash:
		code=new_hash
	else:
		code=makeCode()
	#if code already exist
	qs_exists=Views.objects.filter(viewer=code).exists()
	if qs_exists:
		new_hash=makeCode()
		return createViewer(new_hash)
	return code