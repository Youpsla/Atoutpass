from agent.models import Agent
from users.models import User


# import the logging library
import logging

# Get an instance of a logger
# logger = logging.getLogger(__name__)
logger = logging.getLogger('agent')


def AddAgentContextProcessor(request):
    try:
        user = request.user
        print('User trouve dans le contexte : %s' % (user))
        try:
            current_agent = Agent.objects.get(user_id=user.id)
            print('Agent trouve dans le contexte : %s' % (current_agent))
            # Check if agent form is complete
            if 0 in current_agent.form_state.values():
                agent_form_completed = False
            else:
                agent_form_completed = True
            return {'current_agent': current_agent, 'agent_form_completed': agent_form_completed}
        except Agent.DoesNotExist:
            print "Agent non trouve"
            return {'Agent': None}
    except User.DoesNotExist:
        print "User non trouve"
        return {'User_processor': 'Pas de user'}
