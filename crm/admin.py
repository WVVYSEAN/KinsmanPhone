from django.contrib import admin
from .models import (Contact, Company, Opportunity, TouchPoint, InvitedEmail,
                     UserProfile, Workspace, WorkspaceMembership,
                     EmailThread, AICallLog)


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display  = ('name', 'owner', 'created_at')
    search_fields = ('name', 'owner__email')


@admin.register(WorkspaceMembership)
class WorkspaceMembershipAdmin(admin.ModelAdmin):
    list_display  = ('workspace', 'user', 'role', 'joined_at')
    list_filter   = ('role', 'workspace')
    search_fields = ('user__email', 'workspace__name')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display  = ('name', 'workspace', 'company', 'role', 'email', 'industry', 'source', 'relationship_owner', 'stage')
    list_filter   = ('stage', 'source', 'industry', 'workspace')
    search_fields = ('name', 'company', 'email', 'role')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display  = ('company_name', 'workspace', 'industry', 'funding_stage', 'product_category', 'hq_location', 'stage')
    list_filter   = ('stage', 'industry', 'funding_stage', 'workspace')
    search_fields = ('company_name', 'industry', 'product_category')


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display  = ('company', 'workspace', 'contact', 'service_needed', 'stage', 'estimated_value', 'probability', 'expected_timeline')
    list_filter   = ('stage', 'service_needed', 'workspace')
    search_fields = ('company', 'contact')


@admin.register(TouchPoint)
class TouchPointAdmin(admin.ModelAdmin):
    list_display  = ('touchpoint_type', 'date', 'summary', 'logged_by', 'content_type', 'object_id')
    list_filter   = ('touchpoint_type', 'content_type')
    search_fields = ('summary', 'notes', 'logged_by')


@admin.register(InvitedEmail)
class InvitedEmailAdmin(admin.ModelAdmin):
    list_display  = ('email', 'invited_at')
    search_fields = ('email',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display  = ('user', 'from_email', 'outreach_enabled')
    search_fields = ('user__email', 'from_email')


@admin.register(EmailThread)
class EmailThreadAdmin(admin.ModelAdmin):
    list_display  = ('contact', 'direction', 'subject', 'flagged', 'sent_at')
    list_filter   = ('direction', 'flagged')
    search_fields = ('contact__name', 'contact__email', 'subject', 'body')
    readonly_fields = ('sent_at',)


@admin.register(AICallLog)
class AICallLogAdmin(admin.ModelAdmin):
    list_display  = ('contact', 'input_tokens', 'output_tokens', 'flagged', 'created_at')
    list_filter   = ('flagged',)
    search_fields = ('contact__name', 'contact__email', 'response')
    readonly_fields = ('created_at',)
