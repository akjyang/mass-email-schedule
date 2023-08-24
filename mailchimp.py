import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError
import pandas as pd
from datetime import datetime, timedelta

try:
    mailchimp = MailchimpTransactional.Client('')
    response = mailchimp.users.ping()
    print('API called successfully: {}'.format(response))
except ApiClientError as error:
    print('An exception occurred: {}'.format(error.text))
#%%
mailchimp = MailchimpTransactional.Client('')

test_time = datetime.strptime("2023-08-16 16:00:00", "%Y-%m-%d %H:%M:%S")

test_email = {
    "from_email": "surveys@the-change-lab.org",
    "subject": "Reminder to complete your bonus task",
    "text": "Hi," + "\n" + "\n" +
            "You are receiving this reminder because you completed a previous Prolific study and expressed interest in completing an additional bonus task for $0.40 of bonus compensation." + "\n" + "\n" +
            "This is a reminder that the bonus task is currently open. Please complete the task here: https://wharton.qualtrics.com/jfe/form/SV_08jMLqCdhiCmdka" + "\n" + "\n" +
            "This email was scheduled to send at " + (test_time - timedelta(hours = 4)).strftime("%Y-%m-%d %H:%M:%S"),
    "to": [
      {
        "email": "akjyang@wharton.upenn.edu",
        "type": "to"
      }
    ]
}

def test_run():
  try:
    response = mailchimp.messages.send({"message": test_email})#, "send_at": test_time.strftime(("%Y-%m-%d %H:%M:%S"))})
    print('API called successfully: {}'.format(response))
  except ApiClientError as error:
    print('An exception occurred: {}'.format(error.text))

test_run()
#%%
def send(msg, date_str):
  try:
    response = mailchimp.messages.send({"message":msg, "send_at":date_str})
    print('API called successfully: {}'.format(response))
  except ApiClientError as error:
    print('An exception occurred: {}'.format(error.text))

# only one fixed email body; does not filter for condition
# which means everyone in the csv should be popular/personal condition
def schedule_csv(df, email_col, datetime_col):
    for i in range(len(df)):
        recip = df.at[i, email_col]
        send_date = df.at[i, datetime_col]
        send_date_edt = datetime.strptime(send_date, "%Y-%m-%d %H:%M:%S") - timedelta(hours = 4)
        send_date_edt_string = send_date_edt.strftime("%Y-%m-%d %H:%M:%S")
        email = {
            "from_email": "surveys@the-change-lab.org",
            "subject": "Reminder to complete your bonus task",
            "text": "Hi," + "\n" + "\n" +
                    "You are receiving this reminder because you completed a previous Prolific study and expressed interest in completing an additional bonus task for $0.40 of bonus compensation." + "\n" + "\n" +
                    "This is a reminder that the bonus task is currently open. Please complete the task here: https://wharton.qualtrics.com/jfe/form/SV_08jMLqCdhiCmdka" + "\n" + "\n" +
                    "This email was scheduled to send at " + send_date_edt_string,
            "to": [
                {
                    "email": recip,
                    "type": "to"
                }
            ]
        }
        send(email, send_date)
#%%
test_csv = pd.read_csv("mailchimp_prolific_test.csv")
schedule_csv(test_csv, "id", "send_time")

# list scheduled messages
try:
  response = mailchimp.messages.list_scheduled()
  print(response)
  print(len(response))
except ApiClientError as error:
  print("An exception occurred: {}".format(error.text))

# cancel all scheduled messages
for id in [msg["_id"] for msg in response]:
    try:
        mailchimp.messages.cancel_scheduled({"id":id})
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))