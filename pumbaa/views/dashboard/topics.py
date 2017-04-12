

from pumbaa import models

from flask import Blueprint, render_template
from flask_login import login_required, current_user

module = Blueprint('dashboard.topics', __name__)

from . import dashboard_permission

# @view_config(route_name='manager.topics.index', 
#              permission='member',
#              renderer='/manager/topics/index.mako')
@module.route('/')
@dashboard_permission.require()
def index():
    user = current_user._get_current_object()
    topics = models.Topic.objects(status__ne='delete',
            author=user).all()
    return render_template('/dashboard/topics/index.jinja2',
            topics=topics
            )
    
# @view_config(route_name='manager.topics.problem', 
#              permission='topic',
#              renderer='/manager/topics/problem.mako')
def problem(request):
    topics = models.Topic.objects(status__nin=['delete', 'publish']).all()
    return dict(
                topics=topics
                )

# @view_config(route_name='manager.topics.change_status', 
#              permission='topic', )
def change_status(request):
    topic_id = request.matchdict.get('topic_id')
    status = request.matchdict.get('status')
    
    default_status = ['publish', 'suspend', 'delete']
    if status not in default_status:
        return Response('This status not allow', status='500')
    
    topic = models.Topic.objects.with_id(topic_id)
    if topic is None:
        return Response('Not Found, topic title:%s'%topic_id, status='404 Not Found')
    
    topic.status = status
    topic.save()
    
    if status == 'delete':
        return HTTPFound(location=request.route_path('manager.topics.problem'))
    
    return HTTPFound(location=request.route_path('forums.topics.index'))
