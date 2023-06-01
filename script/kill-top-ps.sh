#!/bin/bash
if [ $(printf "%.0f" "$(ps -eo %cpu --sort -rss | head -n 2 | tail -n 1)") -gt 45 ]; then
  PID=$(ps -eo pid --sort -rss | head -n 2 | tail -n 1)
  echo $PID
  curl -X POST --data-urlencode "payload={\"channel\": \"#newrelic\", \"username\": \"10-10-3-102\", \"text\": \" Top process of Admin_backoffice-Primary-1 Server $PID.\", \"icon_emoji\": \":ghost:\"}" https://hooks.slack.com/services/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
fi
