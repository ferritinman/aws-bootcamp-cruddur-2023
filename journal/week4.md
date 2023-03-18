# Week 4 — Postgres and RDS

## Required Homework/Tasks

### Create RDS Postgres Instance

Creating an RDS Postgres Instance using the CLI was straight forward.  No issues.

### Bash scripting for common database actions

Minor issue with `-e` mentioned during the live session.  I had to use `set -e`

### Install Postgres Driver in Backend Application

No issues installing the Postgres Driver.

### Connect Gitpod to RDS Instance

I had no issues updating the .gitpod.yml file to call a script to update the GitPod environment IP on startup.

### Create Congito Trigger to insert user into database

This was pretty cool triggering AWS Cognito to insert records into an RDS Postgres database table using a Lambda function.  

I could have used an AWS CLI call to create the `AWSLambdaVPCAccessExecuteRole`

This could also be locked down.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeNetworkInterfaces",
                "ec2:DescribeInstances",
                "ec2:DeleteNetworkInterface",
                "ec2:CreateNetworkInterface"
            ],
            "Resource": "*"
        }
    ]
}
```

### Create new activities with a database insert

I encountered the an issue trying to do inserts with the `user_handle` being hardcoded to `andrewbrown`.  

```js 
# app.py

@app.route("/api/activities", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities():
  user_handle  = 'andrewbrown'
  message = request.json['message']
  ttl = request.json['ttl']
  model = CreateActivity.run(message, user_handle, ttl)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return
```

I ended up just hardcoding my own user into here.  I'm not sure if this is an exercise for later on.  I'll fix it if it's not the case.  My ReactJS is terrible at best.


I was getting this error when trying to run INSERTs into the database
```
  File "/backend-flask/lib/db.py", line 120, in print_sql_err
    print ("pgerror:", err.pgerror)
AttributeError: 'NotNullViolation' object has no attribute 'pgerror'
```
I commented out these lines because I think they got deprecated from psycopgp3. I cannot figure out the [psycopg documentation](https://www.psycopg.org/psycopg3/docs/api/errors.html) on how to get it working so I just commented it out for now.

```python
  ## db.py

  def print_sql_err(self, err):
    ...
    ...
    # print the pgcode and pgerror exceptions
    # print ("pgerror:", err.pgerror)
    # print ("pgcode:", err.pgcode, "\n")
```

## Homework Challenges

I didn't have time to work on anything this week.