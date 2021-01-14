#! /usr/bin/env python

"""
Convert a ULog file into CSV file(s)
"""

from __future__ import print_function

import argparse
import os

from .core import ULog

#pylint: disable=too-many-locals, invalid-name, consider-using-enumerate

def main():
    """Command line interface"""

    parser = argparse.ArgumentParser(description='Convert ULog to CSV')
    parser.add_argument('filename', metavar='file.ulg', help='ULog input file')

    parser.add_argument(
        '-m', '--messages', dest='messages',
        help=("Only consider given messages. Must be a comma-separated list of"
              " names, like 'sensor_combined,vehicle_gps_position'"))
    parser.add_argument('-d', '--delimiter', dest='delimiter', action='store',
                        help="Use delimiter in CSV (default is ',')", default=',')


    parser.add_argument('-o', '--output', dest='output', action='store',
                        help='Output directory (default is same as input file)',
                        metavar='DIR')
    parser.add_argument('-i', '--ignore', dest='ignore', action='store_true',
                        help='Ignore string parsing exceptions', default=False)

    args = parser.parse_args()

    if args.output and not os.path.isdir(args.output):
        print('Creating output directory {:}'.format(args.output))
        os.mkdir(args.output)

    #convert_ulog2csv(args.filename, args.messages, args.output, args.delimiter, args.ignore)


def convert_ulog2csv(ulog_file_name, messages, disable_str_exceptions=False):
    """
    Coverts and ULog file to a CSV file.

    :param ulog_file_name: The ULog filename to open and read
    :param messages: A list of message names
    :param output: Output file path
    :param delimiter: CSV delimiter

    :return: None
    """

    msg_filter = messages.split(',') if messages else None

    ulog = ULog(ulog_file_name, msg_filter, disable_str_exceptions)
    data = ulog.data_list

    return_list = list()
    for d in data:
        temp_list = list()
        # print(fmt.format(output_file_name, len(d.data['timestamp'])))
        #with open(output_file_name, 'w') as csvfile:

        # use same field order as in the log, except for the timestamp
        data_keys = [f.field_name for f in d.field_data]
        data_keys.remove('timestamp')
        data_keys.insert(0, 'timestamp')  # we want timestamp at first position

        # we don't use np.savetxt, because we have multiple arrays with
        # potentially different data types. However the following is quite
        # slow...

        # write the header
        columns = data_keys

        # write the data
        last_elem = len(data_keys)-1
        for i in range(len(d.data['timestamp'])):
            inner_temp_list = list()
            for k in range(len(data_keys)):
                inner_temp_list.append(str(d.data[data_keys[k]][i]))
            temp_list.append(inner_temp_list)

        return_list.append((temp_list, columns))
    
    return return_list