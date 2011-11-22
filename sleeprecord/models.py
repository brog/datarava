from django.db import models

# Create your models here.
class Sleeprecord(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    awakenings = models.IntegerField()
    awakeningszqpoints = models.IntegerField(db_column='awakeningsZqPoints') # Field name made lowercase.
    bedtime = models.DateTimeField(db_column='bedTime') # Field name made lowercase.
    grouping = models.IntegerField()
    morningfeel = models.IntegerField(db_column='morningFeel') # Field name made lowercase.
    risetime = models.DateTimeField(db_column='riseTime') # Field name made lowercase.
    startdate = models.DateField(db_column='startDate') # Field name made lowercase.
    timeindeep = models.IntegerField(db_column='timeInDeep') # Field name made lowercase.
    timeindeeppercentage = models.IntegerField(db_column='timeInDeepPercentage') # Field name made lowercase.
    timeindeepzqpoints = models.IntegerField(db_column='timeInDeepZqPoints') # Field name made lowercase.
    timeinlight = models.IntegerField(db_column='timeInLight') # Field name made lowercase.
    timeinlightpercentage = models.IntegerField(db_column='timeInLightPercentage') # Field name made lowercase.
    timeinlightzqpoints = models.IntegerField(db_column='timeInLightZqPoints') # Field name made lowercase.
    timeinrem = models.IntegerField(db_column='timeInRem') # Field name made lowercase.
    timeinrempercentage = models.IntegerField(db_column='timeInRemPercentage') # Field name made lowercase.
    timeinremzqpoints = models.IntegerField(db_column='timeInRemZqPoints') # Field name made lowercase.
    timeinwake = models.IntegerField(db_column='timeInWake') # Field name made lowercase.
    timeinwakepercentage = models.IntegerField(db_column='timeInWakePercentage') # Field name made lowercase.
    timeinwakezqpoints = models.IntegerField(db_column='timeInWakeZqPoints') # Field name made lowercase.
    timetoz = models.IntegerField(db_column='timeToZ') # Field name made lowercase.
    totalz = models.IntegerField(db_column='totalZ') # Field name made lowercase.
    totalzzqpoints = models.IntegerField(db_column='totalZZqPoints') # Field name made lowercase.
    zq = models.IntegerField()
    alarmreason = models.IntegerField(db_column='alarmReason') # Field name made lowercase.
    alarmringindex = models.IntegerField(db_column='alarmRingIndex') # Field name made lowercase.
    dayfeel = models.IntegerField(db_column='dayFeel') # Field name made lowercase.
    sleepgraph = models.CharField(max_length=6144, db_column='sleepGraph') # Field name made lowercase.
    sleepgraphstarttime = models.DateTimeField(db_column='sleepGraphStartTime') # Field name made lowercase.
    sleepstealerscore = models.IntegerField(db_column='sleepStealerScore') # Field name made lowercase.
    wakewindowendindex = models.IntegerField(db_column='wakeWindowEndIndex') # Field name made lowercase.
    wakewindowshow = models.IntegerField(db_column='wakeWindowShow') # Field name made lowercase.
    class Meta:
        db_table = u'SleepRecord'
