import pytest

from lutetium.protocol import MeterMessage, PVMessage
from marshmallow import ValidationError

def test_validation():
    value = 1234
    encoded = MeterMessage.make(value=1234)
    decoded = MeterMessage().loads(encoded)
    assert decoded['value'] == value

    encoded_good = b'''
    {
        "type": "MeterMessage",
        "timestamp": "1970-01-01T12:00:00.073564+00:00",
        "seq": 0,
        "value": 1234.0
    }
    '''

    decoded = MeterMessage().loads(encoded_good)
    assert decoded['value'] == value

    with pytest.raises(ValidationError):
        copy = decoded.copy()
        copy['type'] = 'invalid'
        MeterMessage().load(copy)

    with pytest.raises(ValidationError):
        copy = decoded.copy()
        del copy['type']
        MeterMessage().load(copy)

    with pytest.raises(ValidationError):
        copy = decoded.copy()
        del copy['seq']
        MeterMessage().load(copy)


    encoded_bad = b'''
    {
        "type": "MeterMessage",
        "timestamp": "1970-01-01T12:00:00.073564+00:00",
        "seq": 0,
        "value": "bad value"
    }
    '''

    with pytest.raises(ValidationError):
        decoded = MeterMessage().loads(encoded_bad)

