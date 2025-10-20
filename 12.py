
import requests
from datetime import datetime
import matplotlib.pyplot as plt


params = {
    'starttime': "2000-01-01",
    "maxlatitude": "58.723", 
    "minlatitude": "50.008", 
    "maxlongitude": "1.67",
    "minlongitude": "-9.756",
    "minmagnitude": "1",
    "endtime": "2018-10-11", 
    "orderby": "time-asc"
}
response = requests.get("http://earthquake.usgs.gov/fdsnws/event/1/query.geojson", params=params)
data = response.json()


years = []
magnitudes = []
for earthquake in data['features']:
    timestamp = earthquake['properties']['time']
    dt = datetime.fromtimestamp(timestamp / 1000)
    year = dt.year
    magnitude = earthquake['properties']['mag']
    years.append(year)
    magnitudes.append(year)

print(f"获取了 {len(years)} 个地震事件")


year_counts = {}
for year in years:
    year_counts[year] = year_counts.get(year, 0) + 1


plt.figure(figsize=(12, 6))
plt.bar(year_counts.keys(), year_counts.values(), color='skyblue', edgecolor='navy')


plt.xticks(list(year_counts.keys()), rotation=45)
plt.title('Earthquake Frequency per Year (2000-2018)')
plt.xlabel('Year')
plt.ylabel('Number of Earthquakes')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()

plt.show()

year_magnitudes = {}
for year, mag in zip(years, magnitudes):
    if year not in year_magnitudes:
        year_magnitudes[year] = []
    year_magnitudes[year].append(mag)


avg_by_year = {}
for year, mag_list in year_magnitudes.items():
    avg_by_year[year] = sum(mag_list) / len(mag_list)


sorted_years = sorted(avg_by_year.keys())
sorted_avg = [avg_by_year[year] for year in sorted_years]


plt.figure(figsize=(12, 6))
plt.plot(sorted_years, sorted_avg, marker='o', linewidth=2, markersize=6, 
         color='coral', markerfacecolor='red')
plt.title('Average Earthquake Magnitude per Year (2000-2018)', fontsize=14, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Average Magnitude', fontsize=12)
plt.xticks(sorted_years, rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()