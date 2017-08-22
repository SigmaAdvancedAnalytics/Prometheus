# Prometheus
A dockerized python slackbot used to:  
- [x] Exectute shell commands on the host machine via slack  
- [ ] Trigger terraform updates   
- [ ] Become our own personal Jarvis  

### usage
0) Install docker  
1) Clone repository locally  
2) Replace slackbot information in slack_bot.py with your team/channel info  
3) Run "docker build . -t prometheus"  
4) Run "docker run -d -e SLACKBOT_TOKEN="your_token" prometheus slack_bot.py"  
