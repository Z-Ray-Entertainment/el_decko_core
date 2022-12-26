# El Decko Core
This is the core of El Decko.  
It serves as the glue between any backend, the Stream Deck  and any given user interface.

If writing news user interfaces please target the core instead of using any or multiple  
backends directly.  
Also don't provide Stream Deck related functionality directly in the UI but seek to add  
missing stuff here.

## Develop El Decko
I highly recommend using one shared venv (virtual environment) for all components of El Decko.  
This way you can run `pip install --editable .` on all backends, the core and UIs  
and simply use them as they were properly installed on your system.  
Since in development modules can't be pushed to the pip registry this is, afaik, the best way to   
develop and test all components together.  
Changes on the python code will take effect imminently.  
Only if you change the pyproject.toml files you need to re-run `pip install --editable .` to let this  
changes take effect.