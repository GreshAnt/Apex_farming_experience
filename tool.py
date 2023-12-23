import datetime
import requests


def get_time():
    api_url = "https://worldtimeapi.org/api/timezone/etc/gmt"
    response = requests.get(api_url)
    data = response.json()
    return int(data['unixtime'])


def get_time_stamp(time_stamp):
    if len(str(time_stamp)) > 10:
        time_stamp = int(str(time_stamp)[:10])
    dt_object = datetime.datetime.fromtimestamp(time_stamp)
    time_dict = \
        {
            "Year": dt_object.year,
            "Month": dt_object.month,
            "Day": dt_object.day,
            "Hour": dt_object.hour,
            "Minute": dt_object.minute,
            "Second": dt_object.second
        }
    return time_dict


def num(num_in):
    try:
        num_in = int(num_in)
        if float(num_in - int(num_in)) == 0.0:
            return int(num_in)
        else:
            return num_in
    except TypeError as e:
        return e


def get_time_dict():
    return get_time_stamp(get_time())


if __name__ == '__main__':
    print(get_time_dict())
