from flask import Flask, jsonify
from ast import main
from dotenv import load_dotenv
import os
load_dotenv()
from openai import OpenAI
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import smtplib

from flask_cors import CORS, cross_origin
app = Flask(__name__)

CORS(app, origins=["http://localhost:3000",  "http://assistant-gpt-ui.vercel.app", "https://assistant-gpt-ui.vercel.app/"], expose_headers="*", supports_credentials=True)
# Set up your OpenAI GPT-3 API key


@cross_origin()
@app.route('/send_mail',methods=['POST'])
def assistant_api(request):
  try:
        client = OpenAI()
        data = request.json
    # Define the prompt for the email content
        prompt = "i want you to act as a chief of staff"

        # Additional context or details you want to include in the email
        additional_info = '''in about 150 tokens,
                       {prompt}
                        Do not add subject, and make the salutation Dear {name}
                        end with "Best Regards" on a new line not as a signature, Dont't add a signature'''


        # Combine the prompt and additional information
        input_text = prompt + "\n\n" + additional_info.format(name=data.get('name', ''), prompt=data.get('prompt', ''))

        # Use GPT-3 to generate email content
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=150  ,
            messages=[
            {"role": "system", "content": input_text},
        
        ]
            
        )

        generated_email = response.choices[0].message.content

        # Set up email details
        email_sender = 'evelyn@vela.partners'
        email_receiver = data.get('email', '')
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
            smtp.login(email_sender, os.environ.get("EMAIL_PASS"))
            smtp.sendmail(email_sender, email_receiver,  em.as_string())

        return jsonify({"status": "success", "message": "Email sent successfully!"})

  except Exception as e:
    return jsonify({"status": "error", "message": str(e)})
    

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 8080)))