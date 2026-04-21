from django.conf import settings as django_settings


def workspace_context(request):
    if not request.user.is_authenticated:
        return {}
    from .models import Workspace
    ws_id = request.session.get('active_workspace_id')
    is_master = (request.user.email == django_settings.MASTER_EMAIL)
    if not ws_id:
        return {'active_workspace': None, 'is_master': is_master}
    try:
        from .models import WorkspaceMembership
        ws = Workspace.objects.get(pk=ws_id)
        membership = WorkspaceMembership.objects.filter(workspace=ws, user=request.user).first()
        is_admin = is_master or (membership and membership.role in ('owner', 'admin'))
        from .models import AICallLog
        pending_drafts_count = AICallLog.objects.filter(
            contact__workspace_id=ws_id, status='pending'
        ).count()
        return {
            'active_workspace':     ws,
            'is_master':            is_master,
            'is_workspace_admin':   is_admin,
            'pending_drafts_count': pending_drafts_count,
        }
    except Workspace.DoesNotExist:
        return {'active_workspace': None, 'is_master': is_master, 'is_workspace_admin': is_master}
