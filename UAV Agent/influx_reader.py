import string
from influxdb_client import InfluxDBClient




# https://www.influxdata.com/blog/getting-started-with-python-and-influxdb-v2-0/

# Make sure to change bucket, org, url and token

# Pulls MAVLink message data from InfluxDB
# param [dict] features: MAVLink message and their respected features
# param [string] range: Time range using Flux Query Syntax
# return [dict] data: contains MAVLink message data in the following format:
# {MAVLink Message-feature: [value, value, value]}. Example:
#
# {
#    'VIBRATION-vibration_x': [2.915807595371689e-09, 2.9720885752482218e-09]
#    'ATTITUDE-pitch': [8.801947114989161e-05, 8.925289148464799e-05]
# }
def influx_reader(features, range):

    org = "565ddff2e29c416a"

    client =InfluxDBClient(
        url="http://localhost:9999",
        token="Ad_35XsfmrHT-1mevYf5iuMkWum8NGyCPh2hC3SxvlQdU0wXteCKumFkm5NTrL2dD3bg3JpniiQjW2iBC1kYXw==",
        org=org
    )

    query_api = client.query_api()

    data = {}

    for key, value in features.items():
        for feature in value:
            query = 'from(bucket: "mav")\
              |> range(start: '+ range + ' )\
              |> filter(fn: (r) => r.MAV_message == "'+ key +'")\
              |> filter(fn: (r) => r._field == "'+  feature +'")\
              |> filter(fn: (r) => r._measurement == "my_measurement")'

            result = client.query_api().query(org=org, query=query)
            for table in result:
                results = []
                n=0
                for record in table.records:
                    n+=1
                    results.append(record.get_value())
                    if n==5:
                        break
                data[key+"-"+feature] = results

    return data
