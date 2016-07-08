from flask import Flask
import os
import fnmatch

app = Flask(__name__)

def voltages_file_generator(directory):
    """Search directory for .voltages files and yield one-by-one."""
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.voltages'):
            filepath = os.path.join(root, filename)
            if os.path.isfile(filepath):
                yield filepath

search_dir = '/cephfs'
files = voltages_file_generator(search_dir)


@app.route('/spyking/job')
def spyking_job():
    global files
    next_voltage_file = None
    try:
        next_voltage_file = next(files)
    except StopIteration:
        try:
            files = voltages_file_generator(search_dir)
            next_voltage_file = next(files)
        except:
            return 'No new jobs.'


    return create_return_tuple(next_voltage_file)

def create_return_tuple(next_voltage_file):
    name, ext = os.path.splitext(next_voltage_file)

    return '("{}", "{}")'.format(next_voltage_file, name)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')