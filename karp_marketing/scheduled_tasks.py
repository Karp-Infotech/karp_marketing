import frappe
from frappe.core.doctype.communication.email import make

def send_marketing_emails():

    frappe.log_error("Inside send_marketing_emails")
    
    email_campaign = frappe.get_doc('Regulated Email Campaign',"Outreach")

    if email_campaign.status == "Active":
        print("Active")

        email_template =  frappe.get_doc("Email Template", email_campaign.email_template)

        batch_size = email_campaign.batch_size

        leads = frappe.get_all('Lead', filters={'custom_outreach_email_status': 'Pending'}, limit=10)

        for lead in leads:
            print("Lead Name: " + lead.name)
            lead_doc = frappe.get_doc('Lead', lead.name)
            try:
                make(
                    recipients=lead_doc.email_id,
                    sender="connect@karpinfotech.org",  
                    subject=email_template.subject,
                    content=email_template.response_html,
                    communication_medium="Email",
                    send_email=True
                )
                lead_doc.custom_outreach_email_status="Sent"
                lead_doc.save()
                frappe.db.commit() 

            except Exception as e:
                frappe.log_error(f"Error sending email to lead {lead_doc.name}: {e}")   
    else:
        print("InActive")

    


