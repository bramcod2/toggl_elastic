# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from datetime import datetime, timedelta

import pytz
from tzlocal import get_localzone
from apscheduler.schedulers.blocking import BlockingScheduler
from toggl import api
# from toggl.api_client import TogglClientApi


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# def get_tasks_old():
#     settings = {
#         'token': 'a04011fedbc1d83a167e1a5f600c3650',
#         'user_agent': 'toggl_elastic',
#         'workspace_id': 4921746
#     }
#     toggle_client = TogglClientApi(settings)
#
#     # print(response.json())
#
#     workspaces = toggle_client.get_workspaces().json()[0]
#     print(workspaces)
#     users = \
#         toggle_client.get_workspace_members(workspace_id=settings.get("workspace_id")).json()
#     print(users)
#     user_time = []
#     today = datetime.today()
#
#     yesterday = today - timedelta(days=1)
#     for user in users:
#         time = toggle_client.get_user_hours_range(user_agent=settings.get("user_agent"),
#                                                   workspace_id=workspaces.get("id"),
#                                                   user_id=user.get("id"),
#                                                   start_date=yesterday,
#                                                   end_date=today)
#         user_time.append(time)
#         print(time)
#     print(len(user_time))


def get_tasks():
    last_run = get_last_run("time.txt")
    if last_run:
        passtime = last_run.astimezone(pytz.timezone('UTC'))
    else:
        passtime = datetime(year=1970, month=1, day=1).astimezone(pytz.timezone('UTC'))
    print(passtime)
    list_of_all_entries = api.TimeEntry.objects.all()
    for timeEntity in list_of_all_entries:
        x = timeEntity
        if not timeEntity.is_running:
            if timeEntity.stop > passtime:
                timeEntity = timeEntity.to_dict()
                timeEntity["workspace"] = timeEntity.get("workspace").to_dict()
                if timeEntity["project"] is not None:
                    timeEntity["project"] = timeEntity.get("project").to_dict()
                # timeEntity["tags"] = timeEntity.get("tags").to_dict()
                tags = []
                if timeEntity["tags"] is not None:
                    for tag in timeEntity["tags"]:
                        tags.append(tag)
                    print(tags)

        # if not timeEntity.is_running:

        # if timeEntity.stop is not None and timeEntity.stop > passtime:
        #     print("add to elk")

    write_runtime("time.txt")
    # check if it is running

    # check if it's end time has occurred since last poll

    # print(list_of_all_entries[0])



def write_runtime(dst_file_name):
    """
    Writes the current timestamp to last run file
    :param dstfile: Destination File for Last Run Time
    """
    with open(dst_file_name, 'w+') as dst_file:
        timestamp = str(datetime.timestamp(datetime.now()))
        # LOGGER.debug('\'write_runtime\' - Writing last run time: {}'.format(timestamp))
        dst_file.write(timestamp)


def get_last_run(src_file_name):
    '''
    Gets the last exection time for the alerter
    :param srcfile: source file to read
    :return: datetime object of last execution time or false if no log
    '''
    try:
        # LOGGER.debug('\'get_last_run\' - Loading last run file')
        with open(src_file_name, 'r') as src_file:
            laststamp = src_file.readline()
    except FileNotFoundError:
        print("\'get_last_run\' - Last Run Log Does Not Exist.")
        # LOGGER.debug('Failed to load last run file')
        return False
    local_tz = pytz.timezone(str(get_localzone()))
    datetime_stamp = local_tz.localize(datetime.fromtimestamp(float(laststamp)))
    # LOGGER.info('\'get_last_run\' - Last run file loaded, last run: {}'.format(datetime_stamp))
    return datetime_stamp


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scheduler = BlockingScheduler()

    scheduler.add_job(lambda: get_tasks(), 'interval', seconds=5)

    scheduler.start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
