<!-- Python version- 3.9
django version- 3.1.4

used Django_Rest_framework for creating API : 3.12.2
operating system - Windows 10 

operations performed: -->

input : http://127.0.0.1:8000/metar/ping/
Output(server response) : {"data": 
                                "Pong"}

<!-- getting details of metar information with station code when cache = 1 -->

input: http://127.0.0.1:8000/metar/info/?scode=VOBL&nocache=1

output: {"data":
            {"station": "VOBL", 
            "wind": "090 \u00b0 at the speed of06knots", 
            "last_observation": "2020/12/09at12:30GMT", 
            "temperature": "21\u00b0C(69.8f)", 
            "our_record_time": "2020-12-09T18:11:47.247", 
            "nocache": "1", 
            "fetch_from": "API"}}

<!-- getting details of metar information with station code when cache = 0 -->

input: http://127.0.0.1:8000/metar/info/?scode=VOBL&nocache=0

output: {"data": 
            {"station": "VOBL", 
            "wind": "VRB \u00b0 at the speed of02knots",
            "last_observation": "2020/12/09at20:00GMT", 
            "temperature": "19\u00b0C(66.2f)", 
            "our_record_time": "2020-12-10T01:58:50.091", 
            "nocache": "0", 
            "fetch_from": "CACHE"}}

<!-- output if cache value is not provided -->

input: http://127.0.0.1:8000/metar/info/?scode=VOBL

output: {"msg": "Please set nocache value to 1 for refreshed scode"}