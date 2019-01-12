from datetime import datetime
import schedule
import time

j=0
def do(self, job_func, *args, **kwargs):
    """Specifies the job_func that should be called every time the
    job runs.

    Any additional arguments are passed on to job_func when
    the job runs.
    """
    self.job_func = functools.partial(job_func, *args, **kwargs)
    functools.update_wrapper(self.job_func, job_func)
    self._schedule_next_run()
    return self

def main(j,link):
    print(str(j)+str(link))

def counter():
    link,j = "google.com",0
    print("hello world")
    # while(j < 5):
    #     j += 1
    #     main(j,link)


schedule.every().hour.do(counter)

while True:
    schedule.run_pending()
    time.sleep(5)
