## Installation    
    
Enter your VirusTotal API key to .env file, VT_API_KEY = "ENTER YOUR API KEY HERE"    

```sh
docker-compose up --build
```    
     
In project dir, use this to build.    
     
```sh
127.0.0.1:5000
```     
    
Visit this on browser for ui.       
     
After queueing an URL to scan, it'll take some time to display the results at /results tab.        
Redis queues the URLs, so you can't re-add them for scanning while they're queued or        
the scan is finished just now. 1 hour cooldown, per URL (To save on API calls)       
 
