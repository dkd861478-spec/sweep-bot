import requests,os
K=os.environ["AV_API_KEY"];T=os.environ["TELEGRAM_TOKEN"];C=os.environ["TELEGRAM_CHAT_ID"];P=["EUR/USD","GBP/USD","USD/JPY"]
def g(pair):
 r=requests.get("https://api.twelvedata.com/time_series",params={"symbol":pair,"interval":"5min","outputsize":25,"apikey":K})
 d=r.json()
 if "values" not in d:raise ValueError(str(d))
 return [{"h":float(v["high"]),"l":float(v["low"]),"c":float(v["close"])} for v in reversed(d["values"])]
def swing_low(c):
 for i in range(len(c)-2,1,-1):
  if c[i]["l"]<c[i-1]["l"] and c[i]["l"]<c[i+1]["l"]:return c[i]["l"]
 return min(x["l"] for x in c)
def swing_high(c):
 for i in range(len(c)-2,1,-1):
  if c[i]["h"]>c[i-1]["h"] and c[i]["h"]>c[i+1]["h"]:return c[i]["h"]
 return max(x["h"] for x in c)
def s(pair,k,ref):
 e="🔴" if k=="HIGH" else "🟢";m=e+" <b>SWEEP "+k+" "+pair+"</b>\nNiveau:<code>"+str(round(ref,5))+"</code>"
 requests.post("https://api.telegram.org/bot"+T+"/sendMessage",json={"chat_id":C,"text":m,"parse_mode":"HTML"},timeout=10).raise_for_status()
for pair in P:
 try:
  c=g(pair)
  if len(c)<23:continue
  prev=c[:-2]
  key_low=swing_low(prev[-20:])
  key_high=swing_high(prev[-20:])
  alerted=False
  for cur in [c[-4],c[-3],c[-2]]:
   if cur["l"]<key_low and cur["c"]>key_low:s(pair,"LOW",key_low);print("LOW "+pair);alerted=True;break
   elif cur["h"]>key_high and cur["c"]<key_high:s(pair,"HIGH",key_high);print("HIGH "+pair);alerted=True;break
  if not alerted:print(pair+" ok")
 except Exception as e:print("ERR "+pair+" "+str(e))
