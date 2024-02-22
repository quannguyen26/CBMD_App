# first import the module 
import webbrowser 
  
# then make a url variable 
url = "http://hymetnet.gov.vn/radar/PHA"
  
# getting path 
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
  
# First registers the new browser 
webbrowser.register('chrome', None,  
                    webbrowser.BackgroundBrowser(chrome_path)) 
  
# after registering we can open it by getting its code. 
webbrowser.get('chrome').open(url) 