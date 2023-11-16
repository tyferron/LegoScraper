from apscheduler.schedulers.blocking import BlockingScheduler

def trackerRunner():
    print("Decorated job")

scheduler = BlockingScheduler()
scheduler.add_job(trackerRunner, 'interval', hours=6)
scheduler.start()