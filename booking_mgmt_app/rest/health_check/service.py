from bson import ObjectId
from flask_restplus import marshal

from rest.common.constants import ID, APPLICATION_STATUS_COLLECTION
from rest.health_check.models import application_status
from rest.utils.db_service import Base


class ApplicationStatusService(Base):
    """
    Application Status Service
    """

    def get_application_status(self):

        _count, _application_status = self.get(APPLICATION_STATUS_COLLECTION)
        if _count >= 1 and _application_status:
            return marshal(_application_status[0], application_status)
        else:
            return marshal({"status": "alive"}, application_status)

    def update_application_status(self, req_data):

        _count, _application_status = self.get(APPLICATION_STATUS_COLLECTION)
        if _count >= 1 and _application_status:
            self.update(APPLICATION_STATUS_COLLECTION,
                        query={ID: ObjectId(_application_status[0][ID])},
                        updated_record=req_data)
        else:
            self.create(APPLICATION_STATUS_COLLECTION,
                        req_data)
