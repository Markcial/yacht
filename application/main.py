import shutil
from yacht import Watcher

watcher = Watcher()


def before():
    """
    task that moves the hosts file to the /hosts.d/base location
    :return:
    """
    shutil.copyfile('/hosts', '/hosts.d/base')


def after():
    """
    returns base file to its original location
    :return:
    """
    shutil.copyfile('/hosts.d/base', '/hosts')


def watch():
    before()
    try:
        watcher.start()
    except:
        # log exception
        pass
    after()


if __name__ == '__main__':
    watch()