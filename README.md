# Timekpr-nExT Remote

A python web based interface for easily adding or removing time for users of Timekpr-nExT. The priimary goal is to allow a non-technical parent to use a local (not on the itnernet) web app to:

* require a simple PIN to access the web app
* see current time usage for all users
* add time for a given user
* remove time for a given user

## Current state

vaporware planning stages 

## Notes

* docker for easy running?
* sqlite3 for storage 
* python ssh library: https://www.fabfile.org/

## Related projects

* https://github.com/nvsmirnov/timekprw - defunct as it dependeded on  https://timekprw.ew.r.appspot.com which is dead
* https://timekprw.ew.r.appspot.com - 7 yr old ruby app which uses older timekpr instead of timekpr-next
* https://github.com/frohmut/timekpr-server - "Sample config server implementations and HTML UI for Timekpr"
* https://github.com/frohmut/timekpr - "Timekpr-Sync: Timekpr extension to spread user configurations in the home network"
* https://github.com/cisba/timekpr-cli - "Simple Timekpr CLI" - local python wrapper script

## Development

Development can be done using locally running [LXD containers](https://canonical.com/blog/lxd-virtual-machines-an-overview). After launching an Ubuntu 22.04 container, SSH is enable by default, but only allows key access, so be sure to add your public keys as needed.  From there `adduser` a new user, then run this to install timekpr:

```
sudo add-apt-repository ppa:mjasnik/ppa
sudo apt-get update
sudo apt-get install timekpr-next x11-apps
```

You can then `ssh -X USER@IP` and then run `timekpra` to configure your test users in timekpr via a GUI.  

During development, it's nice to watch the times for a specific user with `watch -n 1 timekpra --userinfo USERNAME`
