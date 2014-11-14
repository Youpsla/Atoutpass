from django.shortcuts import render

# Create your views here.

def AddAgentContextProcessor(request):
    try:
        user = request.user
        print('User trouve dans le contexte : %s' % (user))
        try:
            current_agent = Agent.objects.get(user_id=user.id)
            print('Client trouve dans le contexte : %s' % (current_agent))
            # Check if agent form is complete
            return {'current_agent': current_agent, 'agent_form_completed': agent_form_completed}
        except client.DoesNotExist:
            print "Agent non trouve"
            return {'Agent': None}
    except User.DoesNotExist:
        print "User non trouve"
        return {'User_processor': 'Pas de user'}
