
## Google Drive Downloader
### Quick Start
* Follow the steps in [https://developers.google.com/drive/v3/web/quickstart/python](Google Drive APIs Python Quickstart)
### Code
```
import sckit.downloader.google as scg
cc = scg.get_credentials()
scg.dwnld_with_id( cc, '0B5R9-JLKvJcvN28zUGUzUzFJRlE', 'Model.tar.gz' )
```
