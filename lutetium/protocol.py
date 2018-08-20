import logging
from marshmallow import Schema, fields, validates, ValidationError

logger = logging.getLogger('lutetium.protocol')

class BaseMessage(Schema):
    """Base class for all protocol messages.

    Provides three fields:

     - type: a string with the name of the (sub)class
     - seq: an integer that is optionally checked against the previous
       received value (see validate_seq)
     - timestamp: optional time, for events. Rendered as an ISO8601 string.
    """

    type = fields.Method('get_type', 'set_type', required=True)
    seq = fields.Integer(required=True)
    timestamp = fields.DateTime()

    def get_type(self, obj=None):
        """Returns a string with the name of the current class

        BaseMessage for this one, but normally MeterMessage, etc
        """

        return type(self).__name__

    def set_type(self, value):
        """Minimal class-level type checking"""

        if value != self.get_type():
            raise ValidationError('Invalid object type')

        return value

    @validates('seq')
    def validate_seq(self, value):
        """Optional validator of sequence IDs

        Disables itself if no previous sequence ID is provided in the context,
        otherwise ensures it is the next one. Raises warnings only.
        """

        if self.context.get('seq', 0) == 0:
            return

        expected = self.context['seq'] + 1
        if expected != value:
            logger.warning('%s: Expected sequence ID %s, got %s',
                self.get_type(), expected, value)


class MeterMessage(BaseMessage):
    """Power consumption measurement event"""

    #: Power consumed, in watts
    value = fields.Float(required=True)

class PVMessage(BaseMessage):
    """Combined power consumption and generation event"""

    #: The original value from MeterMessage, power consumed in watts
    meter_value = fields.Float(required=True)

    #: Power generated, in watts
    pv_value = fields.Float(required=True)

    #: Sum of the above
    combined = fields.Float(required=True)
