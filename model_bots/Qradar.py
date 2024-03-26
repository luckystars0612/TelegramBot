from configuration.config import Config
import requests
import logging
import json
import datetime
import schedule
#config file
config = Config()

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Qradar:
    
    def __init__(self) -> None:
        
        self.header = {
            'SEC': config.sec_token,
            'Version': '16.0',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self._ariel_url = 'https://10.79.11.4/api/ariel/searches'
        self._siem_url = 'https://10.79.11.4/api/siem/offenses'
    
    def get_eps_mins(self,time):
        
        query_search = f'SELECT LOGSOURCENAME(logsourceid) AS "LogSource Name", SUM(eventcount) / 30*60 AS "EPS" FROM events GROUP BY LOGSOURCENAME(logsourceid) ORDER BY "LogSource Name" DESC LAST {time} MINUTES'
        try:
            response_searchid = requests.post(self._ariel_url, params={'query_expression': query_search}, headers=self.header, verify=False)
        except Exception as e:
            logging.log(logging.ERROR,e)
            
        if response_searchid.status_code == 201:
            search_id = response_searchid.json()['search_id']
            URL_API = f'{self._ariel_url}/{search_id}'

            while True:
                response_status = requests.get(URL_API, headers=self.header, verify=False)
                if response_status.json()['status'] == 'COMPLETED':
                    break

            URL_API = f'{self._ariel_url}/{search_id}/results'
            try:
                response_result = requests.get(URL_API, headers=self.header, verify=False)
            
                #print(json.dumps(response_result.json(),indent=2))
                return response_result.json()['events']
            except Exception as e:
                logging.log(logging.ERROR,e)
        
    def get_active_offenses(self):
      

        # Set the filter query parameter
        #filter_param = f"follow_up=True and domain_id={domain_id} and start_time>={start_time}"
        filter_param = f"status='OPEN'"
        URL_API = f'{self._siem_url}?filter='+filter_param
        try:
            offenses = requests.get(URL_API, headers=self.header, verify=False).json()
        except Exception as e:
                logging.log(logging.ERROR,e)
                
        with open("test.txt","w",encoding="utf-8") as file:
            file.write(json.dumps(offenses,indent=2))
        file.close()

        return offenses   
    
    def filter_unassign_offense(self,offenses):
        unassign_offenses = []
        for offesne in offenses:
            if not offesne['assigned_to']:
                unassign_offenses.append(offesne)
        return unassign_offenses
    
    def get_detail_offense(self,offense):  

        query_search = 'SELECT * FROM events WHERE INOFFENSE({0}) START {1} STOP {2}'
        
        start_time = offense['start_time']
        last_time = offense['last_updated_time']
        if last_time == start_time:
            dt = datetime.datetime.fromtimestamp(last_time/1000)
            dt+=datetime.timedelta(seconds=1)
            last_time = int(dt.timestamp()*1000)
        query_search = query_search.format(offense['id'],start_time,last_time)
        try:
            response_searchid = requests.post(self._ariel_url, params={'query_expression': query_search}, headers=self.header, verify=False)
        except Exception as e:
            logging.log(logging.ERROR,e)
            
        if response_searchid.status_code == 201:
            search_id = response_searchid.json()['search_id']
            URL_API = f'{self._ariel_url}/{search_id}'
            while True:
                response_status = requests.get(URL_API, headers=self.header, verify=False)
                if response_status.json()['status'] == 'COMPLETED':
                    break

            URL_API = f'{self._ariel_url}/{search_id}/results'
            try:
                response_result = requests.get(URL_API, headers=self.header, verify=False)
                events_in_offense = response_result.json()['events']
            except Exception as e:
                logging.log(logging.ERROR,e)
        print(json.dumps(response_result.json()['event'],indent=2))

        return events_in_offense

 
    def monitor(self):
        current_monitor_offenses = self.get_active_offenses()
        schedule.every(5).minutes.do(current_monitor_offenses)
        
    
q = Qradar()
q.get_active_offenses()
