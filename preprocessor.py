import re
import pandas as pd

def preprocess(data):
    pattern = '\[\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}:\d{2} [APap][Mm]\]'

    message = re.split(pattern, data)[1:]

    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': message, 'message_dates': dates})

    df['message_dates'] = pd.to_datetime(df['message_dates'], format="[%d/%m/%y, %I:%M:%S %p]")

    df.rename(columns={'message_dates': 'dates'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['dates'].dt.date
    df['years'] = df['dates'].dt.year
    df['month_num'] = df['dates'].dt.month
    df['months'] = df['dates'].dt.month
    df['days'] = df['dates'].dt.day
    df['day_name'] = df['dates'].dt.day_name()
    df['hours'] = df['dates'].dt.hour
    df['minutes'] = df['dates'].dt.minute

    period = []
    for hour in df[['day_name', 'hours']]['hours']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df