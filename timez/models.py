from timez import db
from timez.time.utils import TimeKeeper


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_name = db.Column(db.String(255))
    platform = db.Column(db.String(255), nullable=False)
    comment = db.Column(db.String(255))
    location = db.Column(db.String(255))
    zone_name = db.Column(db.String(255))
    utc_offset = db.Column(db.Float)

    def __repr__(self):
        return '<Contact {} from {}>'.format(self.contact_name, self.location)

    @property
    def contact_time(self):
        if self.zone_name:
            return TimeKeeper.get_current_time(self.zone_name)
        elif self.utc_offset:
            return TimeKeeper.get_current_time(self.utc_offset)