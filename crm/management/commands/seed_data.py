from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from crm.models import Contact, Company, Opportunity, TouchPoint, auto_heat


class Command(BaseCommand):
    help = 'Seeds the database with sample data across all pipeline stages'

    def handle(self, *args, **kwargs):
        TouchPoint.objects.all().delete()
        Contact.objects.all().delete()
        Company.objects.all().delete()
        Opportunity.objects.all().delete()

        contacts = [
            # Cold Lead
            dict(stage='cold_lead', name='Alex Turner', email='alex@summitdigital.co', company='Summit Digital', role='Marketing Director', linkedin='https://linkedin.com/in/alexturner', location='Denver, CO', industry='Digital Marketing', source='cold_research', relationship_owner='Jordan Kim'),
            dict(stage='cold_lead', name='Mei Lin', email='mei@pacificbrands.com', company='Pacific Brands', role='CMO', linkedin='', location='Seattle, WA', industry='Consumer Goods', source='cold_research', relationship_owner='Alex Rivera'),
            # Warm Lead
            dict(stage='warm_lead', name='Amara Osei', email='amara@luminarybrands.co', company='Luminary Brands', role='CEO', linkedin='https://linkedin.com/in/amaraosei', location='Los Angeles, CA', industry='Fashion', source='referral', relationship_owner='Alex Rivera'),
            dict(stage='warm_lead', name='Chris Watkins', email='chris@peakflow.media', company='PeakFlow Media', role='Head of Content', linkedin='https://linkedin.com/in/chriswatkins', location='Nashville, TN', industry='Media', source='event', relationship_owner='Jordan Kim'),
            # Discovery Call
            dict(stage='discovery_call', name='Derek Mills', email='derek@velocitysports.com', company='Velocity Sports', role='Director of Brand', linkedin='https://linkedin.com/in/derekmills', location='Austin, TX', industry='Sports & Fitness', source='cold_research', relationship_owner='Jordan Kim'),
            dict(stage='discovery_call', name='Priya Sharma', email='priya@greenfield.com', company='Greenfield Retail', role='CMO', linkedin='', location='Chicago, IL', industry='Retail', source='event', relationship_owner='Alex Rivera'),
            # Proposal
            dict(stage='proposal', name='Nadia Patel', email='nadia@ironclad.tech', company='Ironclad Solutions', role='Head of Partnerships', linkedin='', location='Boston, MA', industry='Legal Tech', source='event', relationship_owner='Jordan Kim'),
            dict(stage='proposal', name='Ben Fowler', email='ben@cascadedigital.com', company='Cascade Digital', role='Growth Lead', linkedin='https://linkedin.com/in/benfowler', location='Portland, OR', industry='SaaS', source='inbound', relationship_owner='Alex Rivera'),
            # Negotiation
            dict(stage='negotiation', name='Marcus Bell', email='marcus@techpulse.io', company='TechPulse Inc.', role='VP of Marketing', linkedin='https://linkedin.com/in/marcusbell', location='San Francisco, CA', industry='SaaS', source='inbound', relationship_owner='Jordan Kim'),
            # Closed Won
            dict(stage='closed_won', name='Sarah Johnson', email='sarah@apexmktg.com', company='Apex Marketing', role='Head of Growth', linkedin='https://linkedin.com/in/sarahjohnson', location='New York, NY', industry='Marketing', source='referral', relationship_owner='Alex Rivera'),
            dict(stage='closed_won', name='Jordan Lee', email='jordan@novabuild.com', company='NovaBuild LLC', role='Founder', linkedin='https://linkedin.com/in/jordanlee', location='Miami, FL', industry='Construction Tech', source='referral', relationship_owner='Jordan Kim'),
            # Closed Lost
            dict(stage='closed_lost', name='Tina Crawford', email='tina@bluehorizon.co', company='Blue Horizon Agency', role='CEO', linkedin='', location='Dallas, TX', industry='Advertising', source='event', relationship_owner='Alex Rivera'),
        ]

        companies = [
            # Cold Lead
            dict(stage='cold_lead', company_name='Summit Digital', website='https://summitdigital.co', industry='Digital Marketing', size='20–50 employees', funding_stage='Bootstrapped', product_category='SEO & PPC', hq_location='Denver, CO', agency_relationships='None known'),
            dict(stage='cold_lead', company_name='Pacific Brands', website='https://pacificbrands.com', industry='Consumer Goods', size='$8M revenue', funding_stage='Seed', product_category='DTC Products', hq_location='Seattle, WA', agency_relationships='None known'),
            # Warm Lead
            dict(stage='warm_lead', company_name='Luminary Brands', website='https://luminarybrands.co', industry='Fashion', size='10–30 employees', funding_stage='Pre-Seed', product_category='Luxury Accessories', hq_location='Los Angeles, CA', agency_relationships='None known'),
            dict(stage='warm_lead', company_name='PeakFlow Media', website='https://peakflow.media', industry='Media', size='$3M revenue', funding_stage='Bootstrapped', product_category='Content Production', hq_location='Nashville, TN', agency_relationships='PR: Spark Comms'),
            # Discovery Call
            dict(stage='discovery_call', company_name='Velocity Sports', website='https://velocitysports.com', industry='Sports & Fitness', size='$5M revenue', funding_stage='Seed', product_category='DTC Apparel', last_funding_date='2024-03-20', hq_location='Austin, TX', agency_relationships='Social: Bold Creative'),
            dict(stage='discovery_call', company_name='Greenfield Retail', website='https://greenfield.com', industry='Retail', size='200+ employees', funding_stage='Growth', product_category='E-commerce', last_funding_date='2022-11-01', hq_location='Chicago, IL', agency_relationships='None known'),
            # Proposal
            dict(stage='proposal', company_name='Ironclad Solutions', website='https://ironclad.tech', industry='Legal Tech', size='$20M ARR', funding_stage='Series B', product_category='Legal Tech SaaS', last_funding_date='2024-09-10', hq_location='Boston, MA', agency_relationships='Content: Prose Studio'),
            dict(stage='proposal', company_name='Cascade Digital', website='https://cascadedigital.com', industry='SaaS', size='$4M ARR', funding_stage='Series A', product_category='Analytics', hq_location='Portland, OR', agency_relationships='None known'),
            # Negotiation
            dict(stage='negotiation', company_name='TechPulse Inc.', website='https://techpulse.io', industry='SaaS', size='$12M ARR', funding_stage='Series A', product_category='Analytics Software', last_funding_date='2023-06-15', hq_location='San Francisco, CA', agency_relationships='PR: Spark Comms'),
            # Closed Won
            dict(stage='closed_won', company_name='Apex Marketing', website='https://apexmktg.com', industry='Marketing', size='50–100 employees', funding_stage='Bootstrapped', product_category='Digital Agency', hq_location='New York, NY', agency_relationships='None known'),
            dict(stage='closed_won', company_name='NovaBuild LLC', website='https://novabuild.com', industry='Construction Tech', size='$7M revenue', funding_stage='Seed', product_category='Project Management SaaS', hq_location='Miami, FL', agency_relationships='None known'),
            # Closed Lost
            dict(stage='closed_lost', company_name='Blue Horizon Agency', website='https://bluehorizon.co', industry='Advertising', size='30–60 employees', funding_stage='Bootstrapped', product_category='Creative Agency', hq_location='Dallas, TX', agency_relationships='Went with competitor'),
        ]

        opportunities = [
            dict(company='Velocity Sports',    contact='Derek Mills',   estimated_value=18000, service_needed='branding',  stage='proposal',    probability=65,  expected_timeline='Q2 2026'),
            dict(company='Luminary Brands',    contact='Amara Osei',    estimated_value=12000, service_needed='packaging', stage='negotiation', probability=80,  expected_timeline='May 2026'),
            dict(company='Ironclad Solutions', contact='Nadia Patel',   estimated_value=35000, service_needed='site',      stage='prospect',    probability=30,  expected_timeline='Q3 2026'),
            dict(company='Cascade Digital',    contact='Ben Fowler',    estimated_value=8500,  service_needed='gtm',       stage='proposal',    probability=50,  expected_timeline='April 2026'),
            dict(company='PeakFlow Media',     contact='Chris Watkins', estimated_value=6000,  service_needed='social',    stage='prospect',    probability=25,  expected_timeline='Q3 2026'),
            dict(company='NovaBuild LLC',      contact='Jordan Lee',    estimated_value=22000, service_needed='branding',  stage='closed_won',  probability=100, expected_timeline='Completed'),
        ]

        for data in contacts:
            Contact.objects.create(**data)
        for data in companies:
            Company.objects.create(**data)
        for data in opportunities:
            Opportunity.objects.create(**data)

        # Sample touchpoints
        contact_ct = ContentType.objects.get_for_model(Contact)
        company_ct = ContentType.objects.get_for_model(Company)

        def tp(ct, obj, tp_type, date, summary, notes='', logged_by=''):
            TouchPoint.objects.create(content_type=ct, object_id=obj.id,
                touchpoint_type=tp_type, date=date,
                summary=summary, notes=notes, logged_by=logged_by)

        sarah  = Contact.objects.get(name='Sarah Johnson')
        marcus = Contact.objects.get(name='Marcus Bell')
        derek  = Contact.objects.get(name='Derek Mills')
        nadia  = Contact.objects.get(name='Nadia Patel')
        amara  = Contact.objects.get(name='Amara Osei')

        tp(contact_ct, sarah, 'email',    '2025-11-10', 'Initial outreach email',          'Sent intro about our branding services', 'Alex Rivera')
        tp(contact_ct, sarah, 'call',     '2025-11-18', '20-min intro call',                'Good fit. Expressed interest in full branding package.', 'Alex Rivera')
        tp(contact_ct, sarah, 'meeting',  '2025-12-02', 'Discovery meeting at their office','Walked through their current brand positioning and goals.', 'Alex Rivera')
        tp(contact_ct, sarah, 'proposal', '2025-12-15', 'Sent proposal — Branding Package', '$42,000 scope for full brand identity + web.', 'Alex Rivera')
        tp(contact_ct, sarah, 'email',    '2026-01-08', 'Follow-up on proposal',            'Asked if they had any questions on the scope.', 'Alex Rivera')
        tp(contact_ct, sarah, 'call',     '2026-01-20', 'Contract call — closed!',          'Agreed on scope and timeline. Contract sent.', 'Alex Rivera')

        tp(contact_ct, marcus, 'linkedin', '2025-12-01', 'Connected on LinkedIn',           'Responded to a post about growth marketing.', 'Jordan Kim')
        tp(contact_ct, marcus, 'email',    '2025-12-10', 'Sent cold intro email',           'Referenced their Series A funding announcement.', 'Jordan Kim')
        tp(contact_ct, marcus, 'call',     '2026-01-05', '30-min discovery call',           'Deep interest in GTM strategy. Requested a proposal.', 'Jordan Kim')
        tp(contact_ct, marcus, 'meeting',  '2026-02-12', 'In-person meeting in SF',         'Presented case studies. Very positive.', 'Jordan Kim')
        tp(contact_ct, marcus, 'proposal', '2026-03-01', 'Proposal sent — GTM & Branding',  '$28,000 over 3 months.', 'Jordan Kim')

        tp(contact_ct, derek,  'email',    '2026-01-20', 'Cold outreach email',             'Personalized around their DTC launch.', 'Jordan Kim')
        tp(contact_ct, derek,  'linkedin', '2026-02-03', 'LinkedIn reply — positive',       'Said they were evaluating agencies in Q1.', 'Jordan Kim')
        tp(contact_ct, derek,  'call',     '2026-03-05', 'Discovery call scheduled',        '45-min call. Good chemistry. Next step: proposal.', 'Jordan Kim')

        tp(contact_ct, nadia,  'event',    '2026-02-15', 'Met at LegalTech Summit NYC',     'Had 20-min chat. Took my card. Very warm.', 'Jordan Kim')
        tp(contact_ct, nadia,  'email',    '2026-02-20', 'Follow-up email post-event',      'Referenced our conversation. Sent capabilities deck.', 'Jordan Kim')

        tp(contact_ct, amara,  'linkedin', '2026-01-10', 'Liked a post + commented',        'Engaged with our branding case study post.', 'Alex Rivera')
        tp(contact_ct, amara,  'email',    '2026-01-25', 'Warm intro email',                'Referenced their Product Hunt launch.', 'Alex Rivera')

        # Company touchpoints
        apex       = Company.objects.get(company_name='Apex Marketing')
        techpulse  = Company.objects.get(company_name='TechPulse Inc.')
        ironclad   = Company.objects.get(company_name='Ironclad Solutions')

        tp(company_ct, apex,      'meeting',  '2025-11-15', 'Onboarding kickoff',          'Intro to team. Set up Slack channel and project board.', 'Alex Rivera')
        tp(company_ct, apex,      'call',     '2026-01-10', 'Monthly check-in Q1',         'Happy with progress. Discussed expanding scope.', 'Alex Rivera')
        tp(company_ct, techpulse, 'email',    '2025-12-05', 'Intro capabilities email',    'Sent deck after Marcus connected us internally.', 'Jordan Kim')
        tp(company_ct, techpulse, 'meeting',  '2026-02-20', 'Exec presentation',           'Presented to CMO + CPO. Strong alignment.', 'Jordan Kim')
        tp(company_ct, ironclad,  'event',    '2026-02-15', 'Met at LegalTech Summit',     'Table conversation turned into follow-up meeting.', 'Jordan Kim')
        tp(company_ct, ironclad,  'email',    '2026-03-01', 'Sent capabilities + pricing', 'Tailored to legal tech vertical.', 'Jordan Kim')

        # Auto-calculate heat for all seeded records
        for c in Contact.objects.all():
            c.heat = auto_heat(c)
            c.save(update_fields=['heat'])
        for co in Company.objects.all():
            co.heat = auto_heat(co)
            co.save(update_fields=['heat'])

        tp_count = TouchPoint.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f'Seeded {len(contacts)} contacts, {len(companies)} companies, '
            f'{len(opportunities)} opportunities, {tp_count} touchpoints.'
        ))
