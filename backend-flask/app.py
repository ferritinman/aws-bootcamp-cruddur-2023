from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import os

from services.home_activities import *
from services.notifications_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *
from services.users_short import *
from services.update_profile import *

from lib.cognito_jwt_token import CognitoJwtToken, extract_access_token, TokenVerifyError

# HoneyComb -----
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

# XRay
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# Cloudwatch
import watchtower
import logging
from time import strftime

# # Configuring Logger to Use CloudWatch
# LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)
# console_handler = logging.StreamHandler()
# cw_handler = watchtower.CloudWatchLogHandler(log_group='cruddur')
# LOGGER.addHandler(console_handler)
# LOGGER.addHandler(cw_handler)

# LOGGER.info('Test log')

import rollbar
import rollbar.contrib.flask
from flask import got_request_exception

# HoneyComb -----
# Initialize tracing and an exporter that can send data to Honeycomb
provider = TracerProvider()

# OTLP sends over the internet
processor = BatchSpanProcessor(OTLPSpanExporter()) 
provider.add_span_processor(processor)


# XRay
xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service='backend-flask', dynamic_naming=xray_url)

# HoneyComb Sends to console (this is noisy)
# simple_processor = SimpleSpanProcessor(ConsoleSpanExporter())
# provider.add_span_processor(simple_processor)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = Flask(__name__)

cognito_jwt_token = CognitoJwtToken(
  user_pool_id=os.getenv("AWS_COGNITO_USER_POOL_ID"),
  user_pool_client_id=os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID"),
  region=os.getenv("AWS_DEFAULT_REGION")
)

# HoneyComb -----
# Initialize automatic instrumentation with Flask
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

# XRay
XRayMiddleware(app, xray_recorder)


frontend = os.getenv('FRONTEND_URL')
backend = os.getenv('BACKEND_URL')
origins = [frontend, backend]
cors = CORS(
  app, 
  resources={r"/api/*": {"origins": origins}},
  headers=['Content-Type', 'Authorization'], 
  expose_headers='Authorization',
  methods="OPTIONS,GET,HEAD,POST"
)

#Cloudwatch logs
# @app.after_request
# def after_request(response):
#     timestamp = strftime('[%Y-%b-%d %H:%M]')
#     LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
#     return response

@app.route('/api/health-check')
def health_check():
  return {'success': True}, 200

#Rollbar
rollbar_access_token = os.getenv('ROLLBAR_ACCESS_TOKEN')
@app.before_first_request
def init_rollbar():
    """init rollbar module"""
    rollbar.init(
        # access token
        rollbar_access_token,
        # environment name
        'production',
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)



# @app.route('/rollbar/test')
# def rollbar_test():
#     rollbar.report_message('Hello World!', 'warning')
#     return "Hello World!"

@app.route("/api/message_groups", methods=['GET'])
def data_message_groups():
  access_token = CognitoJwtToken.extract_access_token(request.headers)

  try:
      claims = cognito_jwt_token.verify(access_token)
      # cognito_jwt_token.claims = cognito_jwt_token.token_service.claims
      # g.cognito_claims = self.claims

      # authenticated request
      app.logger.debug('authenticated')
      app.logger.debug(claims)
      cognito_user_id = claims['sub']
      model = MessageGroups.run(cognito_user_id=cognito_user_id)

      if model['errors'] is not None:
        return model['errors'], 422
      else:
        return model['data'], 200
  except TokenVerifyError as e:
      app.logger.debug(e)
      return {}, 401

@app.route("/api/messages/<string:message_group_uuid>", methods=['GET'])
def data_messages(message_group_uuid):
  access_token = CognitoJwtToken.extract_access_token(request.headers)

  try:
      claims = cognito_jwt_token.verify(access_token)
      # cognito_jwt_token.claims = cognito_jwt_token.token_service.claims
      # g.cognito_claims = self.claims

      # authenticated request
      app.logger.debug('authenticated')
      app.logger.debug(claims)
      cognito_user_id = claims['sub']
      model = Messages.run(
        message_group_uuid=message_group_uuid,
        cognito_user_id=cognito_user_id
      )
      if model['errors'] is not None:
        return model['errors'], 422
      else:
        return model['data'], 200
  except TokenVerifyError as e:
      app.logger.debug(e)
      return {}, 401


@app.route("/api/profile/update", methods=['POST','OPTIONS'])
@cross_origin()
def data_update_profile():
  bio          = request.json.get('bio',None)
  display_name = request.json.get('display_name',None)
  access_token = extract_access_token(request.headers)
  try:
    claims = cognito_jwt_token.verify(access_token)
    cognito_user_id = claims['sub']
    model = UpdateProfile.run(
      cognito_user_id=cognito_user_id,
      bio=bio,
      display_name=display_name
    )
    if model['errors'] is not None:
      return model['errors'], 422
    else:
      return model['data'], 200
  except TokenVerifyError as e:
    # unauthenicatied request
    app.logger.debug(e)
    return {}, 401


@app.route("/api/messages", methods=['POST','OPTIONS'])
@cross_origin()
def data_create_message():
  message_group_uuid   = request.json.get('message_group_uuid',None)
  user_receiver_handle = request.json.get('handle',None)
  print(message_group_uuid)
  print(user_receiver_handle)

  message = request.json['message']
  access_token = CognitoJwtToken.extract_access_token(request.headers)

  print(request.headers)
  print("acess token", access_token)

  try:
      claims = cognito_jwt_token.verify(access_token)
      # cognito_jwt_token.claims = cognito_jwt_token.token_service.claims
      # g.cognito_claims = self.claims

      # authenticated request
      app.logger.debug('authenticated')
      app.logger.debug(claims)
      cognito_user_id = claims['sub']
      if message_group_uuid == None:
        # Create for the first time
        model = CreateMessage.run(
          mode="create",
          message=message,
          cognito_user_id=cognito_user_id,
          user_receiver_handle=user_receiver_handle
        ) 
      else:
        # Push onto existing Message Group
        model = CreateMessage.run(
          mode="update",
          message=message,
          message_group_uuid=message_group_uuid,
          cognito_user_id=cognito_user_id
        )

      if model['errors'] is not None:
        return model['errors'], 422
      else:
        return model['data'], 200
  except TokenVerifyError as e:
      app.logger.debug(e)
      return {}, 401

@app.route("/api/activities/home", methods=['GET'])
@xray_recorder.capture('activities_home')
def data_home():
  # app.logger.debug(request.headers)
  access_token = CognitoJwtToken.extract_access_token(request.headers)
  app.logger.debug(access_token)
  try:
      claims = cognito_jwt_token.verify(access_token)
      # cognito_jwt_token.claims = cognito_jwt_token.token_service.claims
      # g.cognito_claims = self.claims

      # authenticated request
      app.logger.debug('claims')
      app.logger.debug(claims)
      cognito_user_id = claims['username']
      data = HomeActivities.run(cognito_user_id)
  except TokenVerifyError as e:
      _ = request.data
      app.logger.debug(e)
      # unauthentication
      # abort(make_response(jsonify(message=str(e)), 401))
      data = HomeActivities.run()

  return data, 200

@app.route("/api/activities/notifications", methods=['GET'])
def data_notifications():
  data = NotificationsActivities.run()
  return data, 200

@app.route("/api/activities/@<string:handle>", methods=['GET'])
@xray_recorder.capture('activities_users')
def data_handle(handle):
  model = UserActivities.run(handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/activities/search", methods=['GET'])
def data_search():
  term = request.args.get('term')
  model = SearchActivities.run(term)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities():
  user_handle  = 'bayko'
  message = request.json['message']
  ttl = request.json['ttl']
  model = CreateActivity.run(message, user_handle, ttl)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
def data_show_activity(activity_uuid):
  data = ShowActivity.run(activity_uuid=activity_uuid)
  return data, 200

@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities_reply(activity_uuid):
  user_handle  = 'andrewbrown'
  message = request.json['message']
  model = CreateReply.run(message, user_handle, activity_uuid)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/users/@<string:handle>/short", methods=['GET'])
def data_users_short(handle):
  data = UsersShort.run(handle)
  return data, 200

if __name__ == "__main__":
  app.run(debug=True)