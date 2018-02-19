# -*- coding: utf-8 -*-
import typing
from typing import List
import requests
from bs4 import BeautifulSoup
from datetime import datetime


class Controller:
    def __init__(self, cid, name):
        self.cid = cid
        self.name = name


class Booking:
    def __init__(self, **kwargs):
        self.id: str = kwargs.get("id")
        self.station: str = kwargs.get("station")
        self.start_time: datetime = kwargs.get("start_time")
        self.end_time: datetime = kwargs.get("end_time")
        self.controller: Controller = Controller(kwargs.get("cid"), kwargs.get("cname"))
        self.created: datetime = kwargs.get("created")

    def _to_vatbook_format(self):
        return {
            "id": self.id,
            "callsign": self.station,
            "name": self.controller.name,
            "time_start": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "time_end": self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "cid": self.controller.cid
        }

    def update(self):
        # TODO Send to Server
        pass

    def insert(self):
        self.update()


class VatBook:
    def __init__(self):
        self._url = "http://vatbook.euroutepro.com/xml2.php?fir={fir}"

    def get_bookings(self, fir="") -> List[Booking]:
        response = requests.get(self._url.format(fir=fir))
        soup = BeautifulSoup(response.text, "lxml-xml")

        bookings = []

        for booking in soup.find_all("booking"):
            data = {
                "id": booking.id.string,
                "station": booking.callsign.string,
                "start_time": datetime.strptime(booking.time_start.string, "%Y-%m-%d %H:%M:%S"),
                "end_time": datetime.strptime(booking.time_end.string, "%Y-%m-%d %H:%M:%S"),
                "c_id": booking.cid.string,
                "c_name": booking.name.string,
                "created": datetime.strptime(booking.added.string, "%Y-%m-%d %H:%M:%S")
            }

            bookings.append(Booking(**data))

        return bookings
