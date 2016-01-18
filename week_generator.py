from datetime import datetime, timedelta

date = datetime.now()
for i in range(7):
	print date.strftime('%A, %d %b %Y')
	date = date + timedelta(days=1)