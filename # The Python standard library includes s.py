# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json


def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    
    # 修复编码问题：使用UTF-8编码保存文件
    try:
        with open("earthquakes_data.json", "w", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(f"保存文件时出错: {e}")
        # 即使保存失败，也继续执行程序
    
    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    # 数据是GeoJSON格式，我们可以用json解析
    data = json.loads(text)
    return data


def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    # 地震数据在features列表中
    return len(data['features'])


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    # 震级在properties -> mag中
    return earthquake['properties']['mag']


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    # 坐标在geometry -> coordinates中 [经度, 纬度, 高度]
    coordinates = earthquake['geometry']['coordinates']
    longitude = coordinates[0]
    latitude = coordinates[1]
    return latitude, longitude


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    if not data or 'features' not in data or len(data['features']) == 0:
        return 0, (0, 0)
    
    max_magnitude = 0
    max_location = None
    
    # 遍历所有地震事件
    for earthquake in data['features']:
        magnitude = get_magnitude(earthquake)
        
        # 如果找到更大的震级，更新最大值
        if magnitude > max_magnitude:
            max_magnitude = magnitude
            max_location = get_location(earthquake)
    
    return max_magnitude, max_location


# With all the above functions defined, we can now call them and get the result
try:
    data = get_data()
    print(f"Loaded {count_earthquakes(data)} earthquakes")
    max_magnitude, max_location = get_maximum(data)
    print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")
except Exception as e:
    print(f"程序执行出错: {e}")
    print("请检查网络连接或API服务是否可用")