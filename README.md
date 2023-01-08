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

## Development

Development can be done using locally running [LXD containers](https://canonical.com/blog/lxd-virtual-machines-an-overview). After launching an Ubuntu 22.04 container, SSH is enable by default, but only allows key access, so be sure to add your public keys as needed.  From there `adduser` a new user, then run this to install timekpr:

```
sudo add-apt-repository ppa:mjasnik/ppa
sudo apt-get update
sudo apt-get install timekpr-next x11-apps
```

From here you can `ssh -X USER@IP` and then run `timekpra` to configure your test users in timekpr via a GUI.  
