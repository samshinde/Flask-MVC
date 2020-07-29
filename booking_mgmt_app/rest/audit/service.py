from flask_restplus import marshal

from rest.utils.db_service import Base
from rest.common.constants import AUDIT_EVENT

from rest.audit.models import audit_response


class AuditEventService(Base):
    def get_audits(self, page, size, sort_by, order_by, start_date, end_date):
        _count, _audits = self.get(AUDIT_EVENT,
                                   {"meta.created": {
                                       "$gte": start_date,
                                       "$lte": end_date
                                   }},
                                   sort_by=sort_by,
                                   order_by=order_by,
                                   page=page,
                                   size=size)
        return {'records': marshal(_audits, audit_response), 'count': _count}
