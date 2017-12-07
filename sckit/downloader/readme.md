
## Google Drive Downloader
### Quick Start
* Follow the steps in [Google Drive APIs Python Quickstart](https://developers.google.com/drive/v3/web/quickstart/python)
### Setup Crediential
```
python google.py --noauth_local_webserver
```
### Python Code
```
import sckit.downloader.google as scg
cc = scg.get_credentials()
scg.dwnld_with_id( cc, '0B5R9-JLKvJcvN28zUGUzUzFJRlE', 'Model.tar.gz' )
```
