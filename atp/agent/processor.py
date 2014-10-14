from agent.models import Agent
from users.models import User


# import the logging library
import logging

# Get an instance of a logger
# logger = logging.getLogger(__name__)
logger = logging.getLogger('agent')

def AddAgentContextProcessor(request):
    try:
        # current_user = User.object.get_current()
        user = request.user
        print('User trouve dans le contexte : %s' % (user))
        try:
            current_agent = Agent.objects.get(user_id = user.id)
            print('Agent trouve dans le contexte : %s' % (current_agent))
            return {'current_agent' : current_agent}
        except Agent.DoesNotExist:
            print "Agent non trouve"
            return {'Agent' : None}
    except User.DoesNotExist:
        print "User non trouve"
        return {'User_processor': 'Pas de user'}
