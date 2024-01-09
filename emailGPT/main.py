from ast import main
import openai
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import smtplib

# Set up your OpenAI GPT-3 API key
openai.api_key = ''  

# Define the prompt for the email content
prompt = "i want you to act as a chief of staff"

# Additional context or details you want to include in the email
additional_info = '''in about 150 tokens,
                    Send an email to my Barnes, reminding him to send in their weekly plans as we start a new week and motivate him to be productive this week. 
                    Do not add subject, and make the salutation Dear Barnes
                    add "Best Regards" as aclosing '''

# Combine the prompt and additional information
input_text = prompt + "\n\n" + additional_info

# Use GPT-3 to generate email content
response = openai.Completion.create(
    engine="gpt-3.5-turbo-instruct",  
    prompt=input_text,
    max_tokens=150  
)

# Extract the generated email content
generated_email = response.choices[0].text.strip()

# Set up email details
email_sender = 'evelyn@vela.partners'
email_password = 'ahmg eicu fokg utwk'
email_receiver = 'barnes@vela.partners'
email_subject = "Weekly Plan Submission"  
email_signature = '''
Evelyn Kumsah
Chief of Staff
Vela Partners'''
generated_email += email_signature
                   

# Create MIME message for email
em = MIMEMultipart("alternative")
em['from'] = email_sender
em['to'] = email_receiver
em['subject'] = email_subject
em['X--Sender-Signature'] = email_signature

# Attach generated email content to the email body
em_body = MIMEText(generated_email, "plain")
em.attach(em_body)

# Set up SSL context
context = ssl.create_default_context()

# Send the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver,  em.as_string())

print("Email sent successfully!")

if __name__ == "__main__":
    main()