from app import models, db
import datetime

print "Download the image and add it to the image folder"
image_filename = raw_input("Filename ")
nyer_artist = raw_input("artist ")
nyer_contest_number = int(raw_input("NYer contest number "))
start_month = int(raw_input("Start Month "))
end_month = int(raw_input("End Month "))
year = int(raw_input("Year "))
start_day = int(raw_input("Start day "))
end_day = int(raw_input("End day "))
nyer_contest_date = datetime.date(year, start_month, start_day)
contest_number = int(raw_input("Our contest number "))
start_date = datetime.date(year, start_month, start_day)
end_date = datetime.date(year, end_month, end_day)

contest = models.Contest(image_filename=image_filename, nyer_artist=nyer_artist, nyer_contest_number = nyer_contest_number, nyer_contest_date=nyer_contest_date, contest_number=contest_number, start_date=start_date, end_date=end_date)

db.session.add(contest)
db.session.commit()