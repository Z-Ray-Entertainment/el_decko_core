# El Decko Core
This is the core of El Decko.  
It serves as the glue between any backend, the Stream Deck  and any given user interface.

If writing news user interfaces please target the core instead of using any or multiple backends directly.  
Also don't provide Stream Deck related functionality directly in the UI but seek to add missing stuff here.

![El Decko concept](examples/el_decko_concept.svg "El Decko concept")

## Develop El Decko
If you're using virtualenv to develop El Decko I advise to not use separate venvs for each component but to install them  
all in the same environment simply do the following: `pip install --editable .` on all backends, the core and UIs  
and simply use them as they were properly installed on your system.  
Since in development modules can't be pushed to the pip registry this is, afaik, the best way to develop and test all  
components together.  
Changes on the python code will take effect imminently.  
Only if you change the pyproject.toml files you need to re-run `pip install --editable .` to let this  
changes take effect.

### lib-hidapi and flatpak
If you happen to run PyCharm from flatpak (as I do) it will not be able to access `libhidapi-libusb.so` from the host.  
To workaround this issue simply run `pip install --editable .` in a terminal on your host OS which is not sandboxed by  
flatpak.  
Until I found a way to resolve this issue inside the flatpak runtime El Decko can't be provided as a flatpak. :/  
I am really sorry for this.

## Standalone
If you do not want to run El Decko using any UI but just want it to sit silently in the background and waiting for key press events on your Stream Deck you can run it as a stand-alone program after installing it via pip as follows: `ed-core`  
But keep in mind that any change on your configuration files will require you to quit and restart El Decko manually and don't close the terminal window as this might exit the program as well.  

### First run
Upon the first run El Decko Core will create an empty default configurations file at `$XDG_CONFIG/eldecko`.  
The default path is: `$HOME/.config/eldecko`

## Available backends
- [OBS Studio Websocket](https://github.com/Z-Ray-Entertainment/el_decko_backend_obs_ws)
  - Controls OBS Studio via it's build-in Websocket server
- [MPRIS 2](https://github.com/Z-Ray-Entertainment/el_decko_backend_mpris)
  - Controls MPRIS2 compatible media players
  
## Write your own backends / plugins
If you want to write your own backend / plugin for El Decko you do not need to release your code under the same license as the core.  
As El Decko Core searches your python sitelibs for applciations exposing some pre-defined endpoints, but does not change its actual code, your plugin can be distributed under any license you want. This also includes keeping it all for yourself.

The following entry points are searched for: 
- `init`
  - This entry point is invoked for each backend/plugin once uppon booting up El Decko
- `stop`
  - This entry point is invoked once for each backend/plugin when El Decko is shutdown
- `fire`
  - This entry point is invoked for a dedicated backend/plugin once a button on the Stream Deck is pressed
  - Which backend/plugin is to be invoked is defined by the `key_config` of a given key usinbg the `backend` proiperty.
  - The configuration file holding this information is located at: `$XDG_CONFIG/eldecko/streamdeck.json`
- `events`
  - This entry point is not used by any component of El Deck but is intendet to be used in conjunction with user interfaces.
  - The idea is to supply a unified way to query all available events of all available backend/plugins to be exposed inside a UI
  - This could be a drop down allowing to select an backend/plugin plus another drop down to then select a available event supported by the previously selected backend
 
 Addionally ed_core exposed some entry points for backend/plugins to hook into:
 - `start`
   - This entry point is the same entry point which is used to boot up ed_core from CLI
   - It is intendet to be later on used to boot up ed_core from an UI rather than running ed_core manualylö from CLI and then launching any given UI
 - `backends`
   - Retruns a list of all available backends
   - As backends are only loaded as soon as the core is launched this currently conflicts with the above entry point as a UI can not list all available backends if the core isn't already running
