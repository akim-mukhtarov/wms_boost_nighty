## About
A nighty version of currently running [app](http://wsmboost.com) that
is under development to rewrite project in a much more concise and
readable way.  
The goal is to switch from Flask to fastapi, use Redis
for short living objects instead of custom solution and make websocket
handling more convenient.

## Functionality
The project automates daily routine tasks of KazanExpress'
delivery points workers. Thus, it saves up to 2.5 hours every working day.
The tasks are the following:
- Create a refunds report - a dump of detailed info about all refunds
    created within a day. Implemented as a background task (RabbitMQ), the
    progress is available through a websocket connection.
- Storage life cycle steps completion - which ones are briefly just a
    notifications for clients about storage expiration, send via SMS.
    Implemented as a background task (RabbitMQ), the progress is available
    through a websocket connection.
