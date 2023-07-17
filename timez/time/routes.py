from flask import render_template, request, Blueprint
from timez.time.utils import TimeKeeper


time = Blueprint('time', __name__)


@time.route('/time_operations', methods=['POST', 'GET'])
def time_operations():
    if request.method == 'POST':
        if request.form.get('time_data_1'):
            data = request.form.get('time_data_1')
            print(data)
            result = TimeKeeper().get_current_time(data)
            return f'current time in {data} time zone: {result}'
        elif request.form.get('time_data_2'):  # format "EST;00:00"
            data = request.form.get('time_data_2').split(';')
            print(data)
            result = TimeKeeper.time_operation_2(data, 'y')
            return result
        elif request.form.get('time_data_3'):  # format "EST;00:00"
            data = request.form.get('time_data_3').split(';')
            print(data)
            result = TimeKeeper.time_operation_2(data, 'n')
            return result

    return render_template('time_operations.html')
