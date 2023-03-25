# Week 5 — DynamoDB and Serverless Caching

## Required Homework/Tasks

### Data Modelling (Live Stream)
I watched the live stream twice because I wanted to make sure I understood the modelling.  I'm not sure I got it all, but it helped watching it a second time.

I tried to install the NoSQL Workbench but had an issue on my Ubuntu box with it missing FUSE.

```
$  ./NoSQL\ Workbench-linux-3.5.0.AppImage 
dlopen(): error loading libfuse.so.2

AppImages require FUSE to run. 
You might still be able to extract the contents of this AppImage 
if you run it with the --appimage-extract option. 
See https://github.com/AppImage/AppImageKit/wiki/FUSE 
for more information
```

```
$  sudo apt install libfuse2
```

### DynamoDb Utility Scrips
* Implement Schema Load Script
* Implement Seed Script
* Implement Scan Script
* Implement Pattern Scripts for Read and List Conversations

The utilities scripts were straight-forward.  I believe there is an issue with the [seed.sql](../backend-flask/bin/db/seed.sql) because it does have to be loaded twice (for me). 

### Implement Conversations with DynamoDB
* Implement Update Cognito ID Script for Postgres Database
* Implement (Pattern A) Listing Messages in Message Group into Application
* Implement (Pattern B) Listing Messages Group into Application
* Implement (Pattern C) Creating a Message for an existing Message Group into Application
* Implement (Pattern D) Creating a Message for a new Message Group into Application
* Implement (Pattern E) Updating a Message Group using DynamoDB Streams

Implementing Patterns A-D was a fast-paced and I missed a bunch of changes which led to at least 3 hours of debug.

I'm finding the print statements aren't always printing out. I'm assuming we should be using the logger.

Issues included: 
- doubling up the headers with different values and the Bearer token not showing up at all
- returning unformatted JSON
- general bad typing and terrible cut and paste
- there might be an issue with messages not returning formatted JSON in the debug/networking tab but everything seems to work

Implementing DynamoDB Streams was somewhat easy to follow and it was good to see how the troubleshoot the issues with permissions and looking at CloudWatch logs.

## Homework Challenges

The video with Patterns A-D just crushed me, so there was no time to do anything fancy.