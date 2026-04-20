# utils.py

def send_application_notification(applicant_name, applicant_email, opportunity_title):
    """
    Simulate sending a notification after a user submits an application.

    In a real project, this could send an email or notify an admin.
    For this project, we keep it simple and just return a message.
    """
    return f"Notification sent for {applicant_name} ({applicant_email}) applying to {opportunity_title}"