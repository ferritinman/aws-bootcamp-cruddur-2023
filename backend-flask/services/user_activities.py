from aws_xray_sdk.core import xray_recorder

from datetime import datetime, timedelta, timezone
from lib.db import db


class UserActivities:
  def run(user_handle):
    model = {
      'errors': None,
      'data': None
    }

    now = datetime.now(timezone.utc).astimezone()

    if user_handle == None or len(user_handle) < 1:
      model['errors'] = ['blank_user_handle']
    else:
      now = datetime.now()

      sql = db.template('users', 'show')
      results = db.query_object_json(sql, {'handle': user_handle})
      model['data'] = results

    subsegment = xray_recorder.begin_subsegment('mock-data')

    dictionary = {
      "now": now.isoformat(),
      "result-size": len(model['data'])
    }

    subsegment.put_metadata('key', dictionary, 'namespace')
    xray_recorder.end_subsegment()

    return model