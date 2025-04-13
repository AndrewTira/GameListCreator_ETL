import datetime
from airflow.decorators import dag,task
from airflow.models import Variable


@dag(schedule=None, start_date=datetime.datetime(2023, 9 ,1))
def get_variable():
    @task
    def say():
        var_channel = Variable.get('youtube-channel')
        assert var_channel == '@etl-simple'

        message = f'Best channel about ETL is: {var_channel}'
        print(message)

    say()

get_variable_dag = get_variable()

if __name__ == '__main__':
    get_variable_dag.test()
