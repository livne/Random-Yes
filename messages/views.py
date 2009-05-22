import datetime
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_noop
from django.core.urlresolvers import reverse
from django.conf import settings

from messages.models import Message
from messages.forms import ComposeForm
from messages.utils import format_quote

from app.utils import initial_subject, initial_body

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None

def inbox(request, template_name='messages/inbox.html'):
    """
    Displays a list of received messages for the current user.
    Optional Arguments:
        ``template_name``: name of the template to use.
    """
    message_list = Message.objects.inbox_for(request.user)
    return render_to_response(template_name, {
        'message_list': message_list,
    }, context_instance=RequestContext(request))
inbox = login_required(inbox)

def outbox(request, template_name='messages/outbox.html'):
    """
    Displays a list of sent messages by the current user.
    Optional arguments:
        ``template_name``: name of the template to use.
    """
    message_list = Message.objects.outbox_for(request.user)
    return render_to_response(template_name, {
        'message_list': message_list,
    }, context_instance=RequestContext(request))
outbox = login_required(outbox)

def trash(request, template_name='messages/trash.html'):
    """
    Displays a list of deleted messages. 
    Optional arguments:
        ``template_name``: name of the template to use
    Hint: A Cron-Job could periodicly clean up old messages, which are deleted
    by sender and recipient.
    """
    message_list = Message.objects.trash_for(request.user)
    return render_to_response(template_name, {
        'message_list': message_list,
    }, context_instance=RequestContext(request))
trash = login_required(trash)

def compose(request, recipient=None, form_class=ComposeForm,
        template_name='messages/compose.html', success_url=None, recipient_filter=None):
    """
    Displays and handles the ``form_class`` form to compose new messages.
    Required Arguments: None
    Optional Arguments:
        ``recipient``: username of a `django.contrib.auth` User, who should
                       receive the message, optionally multiple usernames
                       could be separated by a '+'
        ``form_class``: the form-class to use
        ``template_name``: the template to use
        ``success_url``: where to redirect after successfull submission
    """
    if request.method == "POST":
        sender = request.user
        form = form_class(request.POST, recipient_filter=recipient_filter)
        if form.is_valid():
            form.save(sender=request.user)
            if request.user.karma == 0:
                request.user.karma = 1;
                request.user.save()
            request.user.message_set.create(
                message=_(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('messages_inbox')
            if request.GET.has_key('next'):
                success_url = request.GET['next']
            return HttpResponseRedirect(success_url)
    else:
        if request.user.suggest_message == True or request.user.karma == 0:
            form = form_class(initial={'subject': initial_subject(request.user), 'body': initial_body(request.user)})
        else:
            form = form_class()
        if recipient is not None:
            recipients = [u for u in User.objects.filter(username__in=[r.strip() for r in recipient.split('+')])]
            form.fields['recipient'].initial = recipients
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))
compose = login_required(compose)

def reply(request, message_id, form_class=ComposeForm,
        template_name='messages/compose.html', success_url=None, recipient_filter=None):
    """
    Prepares the ``form_class`` form for writing a reply to a given message
    (specified via ``message_id``). Uses the ``format_quote`` helper from
    ``messages.utils`` to pre-format the quote.
    """
    parent = get_object_or_404(Message, id=message_id)
    if request.method == "POST":
        sender = request.user
        form = form_class(request.POST, recipient_filter=recipient_filter)
        if form.is_valid():
            form.save(sender=request.user, parent_msg=parent)
            request.user.karma += 1
            request.user.save()
            request.user.message_set.create(
                message=_(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('messages_inbox')
            return HttpResponseRedirect(success_url)
    else:
        form = form_class({
            'body': _(u"%(sender)s wrote:\n%(body)s") % {
                'sender': parent.sender.first_name + ' ' + parent.sender.last_name, 
                'body': format_quote(parent.body)
                }, 
            'subject': _(u"Re: %(subject)s") % {'subject': parent.subject},
            'recipient': [parent.sender,]
            })
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))
reply = login_required(reply)

def delete(request, message_id, success_url=None):
    """
    Marks a message as deleted by sender or recipient. The message is not
    really removed from the database, because two users must delete a message
    before it's save to remove it completely. 
    A cron-job should prune the database and remove old messages which are 
    deleted by both users.
    As a side effect, this makes it easy to implement a trash with undelete.
    
    You can pass ?next=/foo/bar/ via the url to redirect the user to a different
    page (e.g. `/foo/bar/`) than ``success_url`` after deletion of the message.
    """
    user = request.user
    now = datetime.datetime.now()
    message = get_object_or_404(Message, id=message_id)
    deleted = False
    if success_url is None:
        success_url = reverse('messages_inbox')
    if request.GET.has_key('next'):
        success_url = request.GET['next']
    if message.sender.id == user.id:
        message.sender_deleted_at = now
        deleted = True
    if message.recipient.id == user.id:
        message.recipient_deleted_at = now
        deleted = True
    if deleted:
        message.save()
        user.message_set.create(message=_(u"Message successfully deleted."))
        if notification:
            notification.send([user], "messages_deleted", {'message': message,})
        return HttpResponseRedirect(success_url)
    raise Http404
delete = login_required(delete)

def undelete(request, message_id, success_url=None):
    """
    Recovers a message from trash. This is achieved by removing the
    ``(sender|recipient)_deleted_at`` from the model.
    """
    user = request.user
    message = get_object_or_404(Message, id=message_id)
    undeleted = False
    if success_url is None:
        success_url = reverse('messages_inbox')
    if request.GET.has_key('next'):
        success_url = request.GET['next']
    if message.sender.id == user.id:
        message.sender_deleted_at = None
        undeleted = True
    if message.recipient.id == user.id:
        message.recipient_deleted_at = None
        undeleted = True
    if undeleted:
        message.save()
        user.message_set.create(message=_(u"Message successfully recovered."))
        if notification:
            notification.send([user], "messages_recovered", {'message': message,})
        return HttpResponseRedirect(success_url)
    raise Http404
undelete = login_required(undelete)

def publish(request, message_id):
    """
    Declares the message as public. ``message_id`` argument is required.
    No reverse.
    """
    user = request.user
    message = get_object_or_404(Message, id=message_id)
    if (message.sender.id != user.id) and (message.recipient.id != user.id):
        raise Http404
    if message.public == False:
        message.public = True
        message.save()
    return view(request, message_id)
publish = login_required(publish)

def view(request, message_id, template_name='messages/view.html'):
    """
    Shows a single message.``message_id`` argument is required.
    The user is only allowed to see the message, if he is either 
    the sender or the recipient. If the user is not allowed a 404
    is raised. 
    If the user is the recipient and the message is unread 
    ``read_at`` is set to the current datetime.
    """
    user = request.user
    now = datetime.datetime.now()
    message = get_object_or_404(Message, id=message_id)
    if (message.public != True) and (message.sender.id != user.id) and (message.recipient.id != user.id):
        raise Http404
    if message.read_at is None and message.recipient.id == user.id:
        message.read_at = now
        message.save()
    return render_to_response(template_name, {
        'message': message,
        'allow_delete': (message.sender.id == user.id) or (message.recipient.id == user.id),
    }, context_instance=RequestContext(request))
view = login_required(view)
