from .models import Client
from users.models import User


# Create your views here.

def AddClientContextProcessor(request):
    try:
        user = request.user
        print('User trouve dans le contexte : %s' % (user))
        try:
            current_client = Client.objects.get(user_id=user.id)
            print('Client trouve dans le contexte : %s' % (current_client))
            # Check if agent form is complete
            return {'current_client': current_client}
        except Client.DoesNotExist:
            print "Client non trouve dans le contexte"
            return {'Client': None}
    except User.DoesNotExist:
        print "User non trouve"
        return {'User_processor': 'Pas de user'}
