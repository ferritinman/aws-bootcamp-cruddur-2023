# Week 3 — Decentralized Authentication

## Required Homework/Tasks

## Setup Cognito User Pool

I got the opportunity to setup the Cognito User Pools 4x. It was good practice.

### Implement Custom Signin Page

The following is CLI command to remove the "Force change password" state on the "Confirmation status" of manually created users in AWS Cognito

``` bash
 $  aws cognito-idp admin-set-user-password --username victor --password PASSWORD_XYZ --user-pool-id ca-central-1_X5TwbcOqa --permanent
 ```

### Implement Custom Signup Page

No issues with this task as I was following the video.

### Implement Custom Confirmation Page

No issues with this task as I was following the video.

### Implement Custom Recovery Page

No issues with this task as I was following the video.

### Implement backend Flask with JWT (video not on watch list)

No issues with this task as I was following the video.

### Watch about different approaches to verifying JWTs

I watched a video about varying levels of architecting the application with differing levels of coupling/decoupling the Flask application and JWT service.

- Find some articles about side car design patterns

I've been having trouble with running docker compose up with GitPod.  Not exactly sure what is going on.

```
+] Running 0/1
panic: strings: negative Repeat count                0.6s 

goroutine 52 [running]:
strings.Repeat({0x226f8d0?, 0x4?}, 0xc000837640?)
        strings/strings.go:538 +0x438
github.com/docker/compose/v2/pkg/progress.align({0xc0000bc310, 0x66}, {0xc0008460a0, 0xe}, 0x3a)
        github.com/docker/compose/v2/pkg/progress/tty.go:284 +0x1df
github.com/docker/compose/v2/pkg/progress.(*ttyWriter).lineText(0xc0001ec0e0, {{0xc0004b5c70, 0xb}, {0x0, 0x0}, {0x1f83285, 0x7}, 0x0, {0x0, 0x0}, ...}, ...)
        github.com/docker/compose/v2/pkg/progress/tty.go:266 +0xb0c
github.com/docker/compose/v2/pkg/progress.(*ttyWriter).print(0xc0001ec0e0)
        github.com/docker/compose/v2/pkg/progress/tty.go:179 +0x82c
github.com/docker/compose/v2/pkg/progress.(*ttyWriter).Start(0xc0001ec0e0, {0x22926f8, 0xc00005c048})
        github.com/docker/compose/v2/pkg/progress/tty.go:63 +0xa5
github.com/docker/compose/v2/pkg/progress.RunWithStatus.func1()
        github.com/docker/compose/v2/pkg/progress/writer.go:77 +0x30
golang.org/x/sync/errgroup.(*Group).Go.func1()
        golang.org/x/sync@v0.1.0/errgroup/errgroup.go:75 +0x64
created by golang.org/x/sync/errgroup.(*Group).Go
        golang.org/x/sync@v0.1.0/errgroup/errgroup.go:72 +0xa5

 *  The terminal process "/usr/bin/bash '-c', 'docker compose -f "docker-compose.yml" up -d --build'" terminated with exit code: 2. 
 *  Terminal will be reused by tasks, press any key to close it. 
```


## Homework Challenges