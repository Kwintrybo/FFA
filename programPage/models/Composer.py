from datetime import datetime
from typing import Optional
import requests


class NotFoundException(Exception):
    pass


class Composer:
    # TODO: move class variable to distributed cache without eviction (birth and death dates don't change)
    composerDates: dict[str, tuple[datetime, Optional[datetime]]] = {}

    apiPrefix = "https://api.openopus.org"

    def __init__(self, firstName: str, lastName: str):
        self.firstName = firstName
        self.lastName = lastName

    def getDateOfBirth(self) -> tuple[datetime, Optional[datetime]]:
        # Check cache to see if already present
        fullName = f"{self.firstName} {self.lastName}"
        if fullName in self.composerDates.keys():
            print("returning from cache")
            return self.composerDates[fullName]

        # Call OpenOpus API to lookup
        response = dict(requests.get(f"{self.apiPrefix}/composer/list/search/{fullName}.json").json())

        # If composer was not found, then throw exception so they can be manually added to cache
        if response["status"]["success"] == "false":
            raise NotFoundException(f"Composer {fullName} was not found")

        # Otherwise, unwrap and return the birth and death dates
        # TODO: fix assumption that list value 0 is correct
        composer = response["composers"][0]
        birth = datetime.strptime(composer["birth"], "%Y-%m-%d")
        death = None if composer["death"] is None else datetime.strptime(composer["death"], "%Y-%m-%d")
        self.composerDates[fullName] = (birth, death)
        print("returning from API")
        return (birth, death)
