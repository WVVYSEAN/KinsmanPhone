from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('auth/login/',    views.login_page,       name='login'),
    path('auth/google/',   views.google_login,     name='google_login'),
    path('auth/callback/', views.google_callback,  name='google_callback'),
    path('auth/logout/',   views.logout_view,      name='logout'),

    # Workspace management
    path('workspaces/',                  views.workspace_select,        name='workspace_select'),
    path('workspaces/create/',           views.workspace_create,        name='workspace_create'),
    path('workspaces/switch/',           views.workspace_switch,        name='workspace_switch'),
    path('workspaces/<int:pk>/delete/',  views.workspace_delete,        name='workspace_delete'),
    path('master/',                      views.master_panel,            name='master_panel'),

    path('', views.dashboard, name='dashboard'),
    path('settings/', views.settings_view, name='settings'),

    # API routes — must come before the <model_type>/<stage>/ wildcard
    path('api/history/<str:model_type>/<int:pk>/',    views.get_history,    name='get_history'),
    path('api/touchpoint/<str:model_type>/<int:pk>/', views.add_touchpoint, name='add_touchpoint'),
    path('api/create/<str:model_type>/',              views.create_record,  name='create_record'),
    path('api/update/<str:model_type>/<int:pk>/',     views.update_record,  name='update_record'),
    path('api/settings/',                             views.save_settings,  name='save_settings'),
    path('api/send-email/<str:model_type>/<int:pk>/', views.send_email,     name='send_email'),
    path('api/webhook/resend/',                       views.resend_webhook,   name='resend_webhook'),
    path('api/webhook/inbound/',                      views.inbound_webhook,  name='inbound_webhook'),
    path('api/reply/<int:pk>/',                       views.mark_replied,     name='mark_replied'),

    # Email templates & images
    path('api/email-templates/',                      views.email_templates_list,     name='email_templates_list'),
    path('api/email-templates/save/',                 views.email_template_save,      name='email_template_save'),
    path('api/email-templates/<int:pk>/delete/',      views.email_template_delete,    name='email_template_delete'),
    path('api/email-templates/<int:pk>/set-default/', views.email_template_set_default, name='email_template_set_default'),
    path('api/email-templates/<int:pk>/attachments/upload/', views.upload_email_template_attachment, name='upload_email_template_attachment'),
    path('api/email-images/',                         views.email_images_list,        name='email_images_list'),
    path('api/email-images/upload/',                  views.upload_email_image,       name='upload_email_image'),
    path('api/email-images/<int:pk>/delete/',         views.delete_email_image,       name='delete_email_image'),

    # Backup outreach & task status
    path('api/backup-outreach/',                      views.backup_outreach,                   name='backup_outreach'),
    path('api/tasks/<int:job_pk>/status/',             views.task_status,                       name='task_status'),

    # Outreach & template attachments
    path('api/outreach-attachments/upload/',          views.upload_outreach_attachment,        name='upload_outreach_attachment'),
    path('api/outreach-attachments/<int:pk>/delete/', views.delete_outreach_attachment,        name='delete_outreach_attachment'),
    path('api/email-template-attachments/<int:pk>/delete/', views.delete_email_template_attachment, name='delete_email_template_attachment'),

    # AI draft review queue
    path('drafts/',                                   views.ai_drafts,              name='ai_drafts'),
    path('api/ai-drafts/<int:pk>/approve/',           views.approve_ai_draft,       name='approve_ai_draft'),
    path('api/ai-drafts/<int:pk>/reject/',            views.reject_ai_draft,        name='reject_ai_draft'),

    # Workspace member/settings APIs
    path('api/workspace/invite/',                     views.workspace_invite,        name='workspace_invite'),
    path('api/workspace/remove-member/',              views.workspace_remove_member, name='workspace_remove_member'),
    path('api/workspace/logo/',                       views.workspace_update_logo,   name='workspace_update_logo'),


    # Drip campaign
    path('api/drip/<int:contact_id>/generate/',          views.drip_generate, name='drip_generate'),
    path('api/drip/<int:contact_id>/list/',               views.drip_list,     name='drip_list'),
    path('api/drip/<int:contact_id>/pause/',              views.drip_pause,    name='drip_pause'),
    path('api/drip/email/<int:drip_pk>/save-edit/',       views.drip_save_edit, name='drip_save_edit'),
    path('api/drip/email/<int:drip_pk>/send/',            views.drip_send,     name='drip_send'),
    path('api/drip/email/<int:drip_pk>/reject/',          views.drip_reject,   name='drip_reject'),

    # Training data admin
    path('api/training-data/stats/',                    views.training_data_stats,        name='training_data_stats'),
    path('api/training-data/set-model-id/',             views.training_data_set_model_id, name='training_data_set_model_id'),
    path('api/training-data/flag/<int:example_pk>/',    views.training_data_flag,         name='training_data_flag'),

    # Advanced Search (Apify)
    path('leads/advanced-search/',                            views.advanced_search,       name='advanced_search'),
    path('apify/webhook/',                                    views.apify_webhook,         name='apify_webhook'),
    path('apify/run-status/<str:run_id>/',                    views.apify_run_status,      name='apify_run_status'),
    path('apify/search/<int:search_id>/run/',                 views.apify_trigger_run,     name='apify_trigger_run'),
    path('apify/search/<int:search_id>/delete/',              views.apify_delete_search,   name='apify_delete_search'),
    path('apify/search/<int:search_id>/toggle-schedule/',     views.apify_toggle_schedule, name='apify_toggle_schedule'),

    # Contact detail page
    path('contact/<int:pk>/',                          views.contact_detail,                name='contact_detail'),
    path('api/contact/<int:pk>/called/',               views.contact_toggle_called,         name='contact_toggle_called'),
    path('api/contact/<int:pk>/outcome/',              views.contact_set_outcome,           name='contact_set_outcome'),
    path('api/contact/<int:pk>/email-outreach/',       views.contact_toggle_email_outreach, name='contact_toggle_email_outreach'),
    path('api/contact/<int:pk>/financials/',           views.contact_save_financials,       name='contact_save_financials'),
    path('api/contact/<int:pk>/call-notes/',          views.contact_save_call_notes,       name='contact_save_call_notes'),

    # Cold lead list (enhanced search/filter/sort) — must be before wildcard
    path('contacts/cold_lead/',                        views.cold_lead_list,                name='cold_lead_list'),
    path('api/saved-filters/save/',                    views.saved_filter_save,             name='saved_filter_save'),
    path('api/saved-filters/<int:pk>/delete/',         views.saved_filter_delete,           name='saved_filter_delete'),
    path('api/ai-contact-search/',                     views.ai_contact_search,             name='ai_contact_search'),

    # Wildcard — must stay last
    path('<str:model_type>/<str:stage>/', views.stage_list, name='stage_list'),
]
