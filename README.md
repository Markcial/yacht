# yacht
Docker container that updates hosts file with new container entries upon docker event changes

# Usage
Install the yacht service file via `sudo systemctl enable service/yacht.service` and then start it via `sudo systemctl start yacht.service` or `sudo service start yacht`.

You can check the service status via `journalctl -f -u yacht` or `sudo service yacht status` or `sudo systemctl status yacht`, you will get a display similar to this one: 

![Yacht status sample](http://i.imgur.com/PtcoEtA.png)

It will look for any event changes on the docker boxes and write those changes on your `/etc/hosts` file.

Once you have created a new box with hostname property, it will be reflected on your new hosts file.

Example: 

`docker run -d --name foo.bar debian sleep infinity`
`cat /etc/hosts` => 172.17.0.5 foo.bar

**Is very important to keep a backup of your hosts file aside. This library is doing constant writes on the hosts file on any docker event change for the newly created or erased boxes**
