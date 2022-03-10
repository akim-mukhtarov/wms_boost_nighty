import datetime
import pytz


class ClientTime:
    """ Handles datetime operations in specified timezone """
    def __init__(self, timezone):
        self._timezone = timezone
        self._today_date = None

    def get_today_date(self) -> datetime.date:
        if self._today_date:
            return self._today_date

        tz = self._timezone
        today_utc = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        today_date = today_utc.astimezone(tz).date()
        self._today_date = today_date
        return self._today_date

    def get_days_dif(self, date) -> int:
        today_date = self.get_today_date()
        delta = today_date - acceptance_date
        return delta.days

    def get_days_ago(self, days) -> datetime.datetime:
        n_days_ago = self.get_today_date() - datetime.timedelta(days)
        # build new datetime (since datetime.date does not provide timestamp method)
        dt = datetime.datetime(
            year=n_days_ago.year,
            month=n_days_ago.month,
            day=n_days_ago.day,
        )
        # reinterpret in client's timezone !
        dt = self._timezone.localize(dt)
        return dt
