import requests
import json
import time
from random import randrange, randint

urlapi = "https://www.999doge.com/api/web.aspx"
headers = {
    "Origin": "file://",
    "User-Agent": "Android Phone / Chrome 65 [Mobile]:Mozilla/5.0 (Linux; Android 8.0; BLA-L29 Build/HUAWEIBLA-L29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3236.6 Mobile Safari/537.36",
    "Content-type": "application/x-www-form-urlencoded",
    "Accept": "*/*",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    "X-Requested-With": "com.reland.relandicebot",
}

def runlowhigh(percent, bet):
    global high
    global low
    c = str(999999 * float(percent) / 100)
    if (bet == "HI"):
        n = str(c.split(".")[1])
        rank = 6 - len(n)
        low = int(int(n) * (10 ** rank))
        high = 999999
    if (bet == "LOW"):
        low = 0
        high = int(c.split(".")[0])

data = open("data.json")
d = json.loads(data.read())

baseBet = { }
maxBet = { }
minChance = { }
maxChance = { }
maxRollWin = { }
mulWin = { }
mulLose = { }
ifWinBaseBet = { }
ifLoseBaseBet = { }

nextChance = { }
nextRoll = { }
payIn = { }
payOut = { }

maxNo = 0
ifbalancewd = float(d['withdraw']['balance'])

for arrd in d['runbot']:
    baseBet[maxNo] = float(arrd['baseBet'])
    maxBet[maxNo] = float(arrd['maxBet'])
    minChance[maxNo] = float(arrd['minChance'])
    maxChance[maxNo] = float(arrd['maxChance'])
    maxRollWin[maxNo] = int(arrd['maxRollWin'])
    mulWin[maxNo] = float(arrd['mulWin'])
    mulLose[maxNo] = float(arrd['mulLose'])
    ifWinBaseBet[maxNo] = int(arrd['ifWinBaseBet'])
    ifLoseBaseBet[maxNo] = int(arrd['ifLoseBaseBet'])

    nextChance[maxNo] = randrange(minChance[maxNo], maxChance[maxNo])
    nextRoll[maxNo] = 0
    payIn[maxNo] = baseBet[maxNo]
    maxNo += 1

def runbot(username, password, apikey):
    sessCookie = ""
    balance = 0
    checklogin = False
    amountProfit = 0
    no = 1
    noarr = 0
    data = {
        "a": "Login",
        "Key": apikey,
        "Username": username,
        "Password": password,
        "Totp": ""
    }
    r = requests.post(urlapi, data, headers)
    jsn = json.loads(r.text)
    if (jsn['SessionCookie']):
        balance = jsn['Doge']['Balance'] / (10 ** 8)
        sessCookie = jsn['SessionCookie']
        checklogin = True
        print('---------------------------------------------------------------------------\n')
        print('LOGIN SUCCESS\n')
        print('Donate me: DTJyhEQRJ6fkr9XCdDT9EqeFtvRWJ3bJLZ\n')
        print('Balance now: ' + str(balance) + ' Doge\n')
        print('---------------------------------------------------------------------------\n')
        totalprofit = float(balance)
    if (checklogin == True and sessCookie != "" and balance != 0):
        while True:
            try:
                numtaruhan = randrange(0, 9)
                if (numtaruhan >= 0 and numtaruhan <= 4):
                    vartaruhan = "LOW"
                else:
                    vartaruhan = "HI"
                nextChance[noarr] = randrange(minChance[noarr], maxChance[noarr])
                runlowhigh(nextChance[noarr], vartaruhan)
                dataplay = {
                    "a": "PlaceBet",
                    "s": sessCookie,
                    "PayIn": int(payIn[noarr] * (10 ** 8)),
                    "Low": low,
                    "High": high,
                    "ClientSeed": randint(0, 999999),
                    "Currency": "doge",
                    "ProtocolVersion": "2",
                }
                d = requests.post(urlapi, dataplay, headers)
                djsn = json.loads(d.text)
                if (djsn['BetId']):
                    payOut[noarr] = round(float(djsn['PayOut']) / (10 ** 8), 8)
                    profit = payOut[noarr] - payIn[noarr]
                    profit = round(profit, 8)
                    amountProfit += profit
                    amountProfit = round(amountProfit, 8)
                    print(str(no) + ' - [' + vartaruhan + '] Bet(' + str(payIn[noarr]) + ') Profit(' + str(profit) + ') TotalProfit(' + str(amountProfit) + ')\n')
                    no += 1
                    if (profit > 0):
                        payIn[noarr] *= mulWin[noarr]
                        nextRoll[noarr] += 1
                        if ((maxRollWin[noarr] > 0 and nextRoll[noarr] > maxRollWin[noarr]) or ifWinBaseBet[noarr] == 1):
                            nextRoll[noarr] = 0
                            payIn[noarr] = baseBet[noarr]
                    else:
                        payIn[noarr] *= mulLose[noarr]
                        if (payIn[noarr] > maxBet[noarr] or ifLoseBaseBet[noarr] == 1):
                            nextRoll[noarr] = 0
                            payIn[noarr] = baseBet[noarr]
                    payIn[noarr] = round(payIn[noarr], 8)
                    noarr += 1
                    if (noarr >= maxNo):
                        noarr = 0
                    totalprofit = balance + amountProfit
                    if (totalprofit >= int(ifbalancewd)):
                        datawd = {
                            "a": "Withdraw",
                            "s": sessCookie,
                            "Amount": d['withdraw']['wdbalance'],
                            "Address": d['withdraw']['address'],
                            "Totp": "",
                            "Currency": "doge"
                        }
                        runwd = requests.post(urlapi, datawd, headers)
                        rwd = json.loads(runwd.text)
                        if (rwd['Pending']):
                            print("Withdraw amount " + d['withdraw']['wdbalance'] + " Doge is success\n")
            except:
                print("Disconnect...")
                break
    else:
        print('Username or password is wrong')

runbot(d['account']['username'], d['account']['password'], 'b9ec1975be6b4ae8a5e7e3da4abeb17b')