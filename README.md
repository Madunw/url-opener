# url-opener
url-multiple-opener using chromedriver/selenium. 

## Install
### Download chromedriver:
```
pip install selenium
```
### Download chromedriver:
https://chromedriver.chromium.org/downloads

## Usage
Save the links in **url.txt**   

### Run
```
python opener.py [opts]
```
## Options
set proxy in **proxy_config.py**   
|  opts   | Explanation  |
|  ----  | ----  |
| -c  | Automatic close browser |
| -i   [arg]  | Interval time(arg: second) |
| -pn  | No authentication proxy on |
| -pa  | Authentication proxy |
 
