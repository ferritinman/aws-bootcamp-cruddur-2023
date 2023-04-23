# Week 8 — Serverless Image Processing

## Required Homework/Tasks

### Serverless Image Processing
During the live stream, I was introduced to the AWS CDK to start the implementation for processing images to smaller images (using Lambda triggered by S3 events).

The CDK project was written in TypeScript and deployed in the AWS backend using CloudFormation (via CDK)

Here are a few links from the live stream that might be useful:
* [https://constructs.dev](https://constructs.dev)

* [https://docs.aws.amazon.com/cdk](https://docs.aws.amazon.com/cdk)

* [https://thecdkbook.com](https://thecdkbook.com)

* [https://www.cdkday.com](https://www.cdkday.com)


You will need to bootstrap your account once per account per egion for CDK CLI commands to work. 
```
$ cdk bootstrap "aws://818240358603/ca-central-1"
```

Commands to deploy out CDK projects
```
# Creates CloudFormat yaml file in ./json
$ cdk synth


$ cdk deploy
```

Utility scripts were built to help delete and upload files to S3 to facilitate easier testing.

At the end of the two videos, the CDK project creates two buckets (original and procssed images.)  Once an image is uploaded to the "original" S3 bucket, an S3 event triggers the Lambda to use JS library "sharp" to make a thumbnail picture and upload that image to the "processed" S3 bucket.  Also of note is that policies were added to allow permissions to write to the S3 buckets and execute the Lambda.

#### Issues
After refactoring the architecture to use two buckets instead of one, I started a new Gitpod environment and redeployed the "thumbing-serverless-cdk" project.  Unfornately, there was a bug in the [/bin/avator/build](../bin/avatar/build) fixed in this [revision](https://github.com/ferritinman/aws-bootcamp-cruddur-2023/commit/77b4a703a4802fde7fe148f70e8ca3530cc8c374) where the node_modules are being put in the wrong directory.  I found the following error in CloudWatch logs.

![](assets/week08/sharp_issue.png)


### Serve Avatars via CloudFront

CloudFront is a CDN and that we will be using to host assets for our avator thumbnails.  This was configured manually through the AWS console.

I had to regenerate the SSL certificate in us-east-1 because CloudFront is a global AWS service, but the previous certificate generated for the ALB was in ca-central-1.

Also, a DNS A record was created with the Alias pointed ot CloudFront.

My avatar can be found here:

[https://assets.ferritinman.com/avatars/skeletor.jpg](https://assets.ferritinman.com/avatars/skeletor.jpg)


### Implement Users Profile Page

I did a bunch of JS coding and CSS styling around implementing the User profile page while following the video.  Nothihg crazy here just a lot of typing mistakes.


### Implement Migrations Backend Endpoint and Profile Form

I followed along on the video implementing a database migratations framework.  It's a similar concept to "flyway" for Spring Boot. In this case, we used it to add a "bio" column to the "users" table.

I also did a bunch more JS coding and CSS styling around the User Profile page.

### Implement Avator Uploading

I rode the struggle bus really hard on this section.  I'm 2.5 weeks behind now. Ugh.

In this section, the goal was to get the pre-signed URL for S3 to upload the image.  The trouble is getting CORS to work.

I was not able to get it working with Bayko's solution with API Gateway route with OPTIONS {proxy+} configuration. 

I hacked around the {proxy+} configuration for hours and danced around it assumning I would get it working by re-watching the video and doing it slowly. I found some typing mistakes like:

"back" instead of "bucket"
![](./assets/week08/s3_bucket_back.png)

Lambda function "CruddurApiGatewayLambdaAuthorizer" did not have the environment variables set for "CLIENT_ID" or "USERPOOL_ID" which I think was this:
![](./assets/week08/authorizer_match.png)

After a long time, I gave up on getting the video solution working and studied up a bit.

I came across some helpful links:
* [https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-cors.html](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-cors.html)
  - "If you configure CORS for an API, API Gateway ignores CORS headers returned from your backend integration."
  - This got me thinking "Why do we return headers from Lambda function CruddurAvatarUpload if it gets ignored"
  - I ended up removing it in this [revision](https://github.com/ferritinman/aws-bootcamp-cruddur-2023/commit/a03ad3eb963bbc4d77dd9ecddb9eeb7c44771a50). 
* [https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/204](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/204)
  - The 204's seem to be okay ... this is what OPTIONS was returning
* [https://stackoverflow.com/questions/61188770/cors-impossible-on-aws-lambda-http-api-gateway-integration](https://stackoverflow.com/questions/61188770/cors-impossible-on-aws-lambda-http-api-gateway-integration)
  - This guided me through what options to add on the CORS section
* [https://repost.aws/knowledge-center/api-gateway-internal-server-error](https://repost.aws/knowledge-center/api-gateway-internal-server-error)
* [https://repost.aws/knowledge-center/api-gateway-cloudwatch-logs](https://repost.aws/knowledge-center/api-gateway-cloudwatch-logs)
  - Not sure I got much into this page ... but maybe if I kept failing I would have gone through it.

This is what I came up with:
![](./assets/week08/api_gateway_cors.png)

In API Gateway, I removed the "Authorization" to help me isolate the "CruddurAvatorUpload" Lambda function. Once I got that working, I added "Authorization" back in and I troubleshot that until I got it working.

Screenshots are limited as I got moving "quickly" after I got CORS working via API Gateway.

I got tired of clicking the ugly green button so I made a quick "curl" command.

```
$ curl -v -X POST https://xxxyyyzzz.execute-api.ca-central-1.amazonaws.com/avatars/key_upload \
    -H "Origin: https://f3000-ferritinman-awsbootcamp-.....gitpod.io" \
    -H "authorization: Bearer eyJraWQiO..." \
    -H "Accept: application/json" \
    -H "content-type: application/json"
```

The Bearer token was taken using the request header "authorization" from DevTools.  It seemed to last "forever" so I used it for "a while".

I kept getting a lot of these which was not super helpful, but I was getting them quicker than clicking on website.
```
{"message":"Internal Server Error"}

```

Ugh, so annoying.

![](./assets/week08/authorizer_1_jwt_parts.png)

I had a feeling the "Bearer" part needed to be parsed out from a previous conversation with ChatGPT which led to this [https://github.com/ferritinman/aws-bootcamp-cruddur-2023/commit/de69c8c13af8aacd7cf4531f1eb893928707a8c5](revision).

![](./assets/week08/chat_gpt_bearer.png)

Getting close ... token was just expired.

![](./assets/week08/authorizer_2_jwt_expired.png)

Finally ended up with this, which was amazing!
```
{"status_code":200,"body":"{\"url\":\"https://xxx-yyy-zzz-ferritinman.s3.ca-central-1.amazonaws.com/mock.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA35AXNBDF6C2JV5XX%2F20230423%2Fca-central-1%2Fs3%2Faws4_request&X-Amz-Date=20230423T070511Z&X-Amz-Expires=300&X-Amz-Security-Token=IQoJb3JpZ2luX2VjENf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDGNhLWNlbnRyYWwtMSJHMEUCIBd2192N8IKzXREZDEm124Er5b26qeP8SSbt12QtFi1ZAiEAgt9hbN8yNLUoQ1bwR9TwgUJH7uNkN4OOR2hjWiL9BjcqhgMI0P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw4MTgyNDAzNTg2MDMiDHRDO22tJOSM7Yg5OSraAjKG9VFZSCPY9DojlHQy5P3ZQnAoHJTcPme8Oo1UsZqyKnGpowz554h%2FdEXm6tB%2FK0yjUckalUz4%2FhpRC8HI1nak6%2Br4utR3GK6%2Fbqkmqvskll4Jeheg1lkTlCOJCZMsYykSXMHsxh%2B4afC9gI28CtSc%2FSTiuMmAkXPKwr5p52Ibcey3qW%2FtzNaezv9kur5HOHHSYQR2Jc8%2FHZdbfi7vLJXRD6Z6RyZ9XlDZrxAGHx6aakuEY770jRAtC42OojauYTDIly%2FASTr%2BKORbmz8uSnXafXuTt94XOnMtUhHib9dPC1WIgE0wwA99FTWc4%2B2dDpac6kmIvSSzAhCqGYbul59IUqx1SIxZfVYunm%2BgRwNGw77kXvWBwJMA0B9SwL61qXT68RW6XpJWitCn7Ut3Fm2CvQ1cu5iWY1NZ7GaLJZCSkw6Eb5OZreyuaAqU* TLSv1.2 (IN), TLS header, Supplemental data (23):
* TLSv1.2 (IN), TLS header, Supplemental data (23):
* Connection #0 to host xxxyyyzzz.execute-api.ca-central-1.amazonaws.com left intact
0zmC7%2BaO0cYTN47%2BmGsw8bCTogY6ngFHFz51qsyp0q9JhwQZt5msTaIQlcMpQp7pq9JQ7vaX4doqGHHNe8t8E%2B%2FTet7VcxCETtOoLuBUsejGXx7zQFdVyqzef2y5arfs5zA7rjaEdDyWrLoukxPV5Rrf4%2B3zuYqWN7jFWb%2Bdz2SqUaPwLFS2u5hecoXm8AMgQFBPD1B7Ah3I7Q%2F9JUERpszPAUBTS5fUjtIJhK%2Fd4Xf2M6DwTQ%3D%3D&X-Amz-SignedHeaders=host&X-Amz-Signature=c5fec1828b6285e9557500e6f7b92bc4d53af554d633899f6a3c5881aa029406\"}"}
```

![](./assets/week08/authorizer_3_jwt_success.png)

This makes a lot of more sense to me than the video solution (plus it actually works for me).  I hope its "correct", there are always more than one way to do things in cloud.

Notes:
- API Gateway | Develop | CORS requires new gitpod URL 
- ProfileForm.js need new gitpod URL (I tried it without and it works)

