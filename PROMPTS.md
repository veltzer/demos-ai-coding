# Prompts

1. Run a background task that print "I'm still here" with a number every 5 seconds to /dev/pts/6.
2. stop the background task
3. Run a background subagent that prints "Hey, you got an email!" with the title of the email to /dev/pts/6 when ever I get an email in gmail via polling on the gmail mcp and not via cron but rather by sleeping 10 seconds between each query.
4. kill the subagent
5. Run a background subagent that prints "I'm still here" with a number to /dev/pts/6 every 5 seconds. Do that with sleeps and not via cron.
6. kill the subagent
