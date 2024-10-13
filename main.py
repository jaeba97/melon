import melon-ticket-alert

def main() -> None:
    seats = get_seats_summary()
    messages = check_remaining_seats(seats['summary'])
    send_message(messages)

def get_seats_summary() -> None:
    url = "https://ticket.melon.com/tktapi/product/block/summary.json?v=1" 
   
    body = {
        'prodId': '210441',
        'pocCode': 'SC0002',
        'scheduleNo': '100001',
        'perfDate': '20241026',
        'seatGradeNo': '10008',
        'corpCodeNo': ''
    }

    header = {
        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Content-Length': '71',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '_fwb=106kGcIJnPuco213Ez9LHo1.1728313951411; PC_PCID=17283139512342114238715; _T_ANO=J4FhNy2MoyR2be5if1X+K7rRGpVtakymheoRHjxukUPp2Z6p0KXerKSiZNmckmTvUNnxY3oGT/ZsKqGMPXcRQxAMk/XnzlDAhIkTzajjIbeQRpa6Mb5FUl8gsKfYWcs6PWRXPYrlKgnoEV+7dBMYUMJ22zgokX96mEq5ED3c5FojBqtQs50/2aI3bGZYnhi/WTKXvw6ombVpw5vm4hTcsUvlCNV/UJ2ZKu4N18RZj4SWAFRbHkUfIPblgyPGyW7VpCtDjf8Dj9r81gtVl6v4lhp5mV/VxRqOWg+/vkwaOJdg4+MvS3N0eq/g2MZByL3gyWbeHHxYiyPRAlC1ewaKKA==; melonlogging=1000000698; TKT_POC_ID=WP15; cbo=0; MAC=fz3d6tR6Jaujw8p5F+hFt918UYt/H4pK1BwOVFRG7thgBtrpkigy4BFI7olBtIjs; MLCP=NjQ2NzYxMTclM0Jqa2NvbXNnJTNCJTNCMCUzQmV5SmhiR2NpT2lKSVV6STFOaUo5LmV5SnBjM01pT2lKdFpXMWlaWEl1YldWc2IyNHVZMjl0SWl3aWMzVmlJam9pYldWc2IyNHRhbmQwSWl3aWFXRjBJam94TnpJNE56azFNelF3TENKdFpXMWlaWEpMWlhraU9pSTJORFkzTmpFeE55SXNJbUYxZEc5TWIyZHBibGxPSWpvaVRpSjkubjhCbVFIU2hlekUycExqQ0tIRmhCN2Z6ZFZxNWVGamZjYUhvclNPY1k0YyUzQiUzQjIwMjQxMDEzMTM1NTQwJTNCJUVDJTk2JUI0JUVDJUE5JTk0JUVDJUE2JTg4JUVCJThCJTg4JTNCMSUzQmprY29tc2clNDBuYXZlci5jb20lM0IzJTNC; MUS=-1092284878; keyCookie=64676117; store_melon_cupn_check=64676117; NetFunnel_ID=5002%3A200%3Akey%3D94DB0690A1D88E693E0AF2328FF96AF3DB4D75955BEAB9407DEE40BFEAE0450FD31449C7E565F82012F52F4ECFC38856E02CC5AB52B15A016B5772DB9BD6BFEFEAA18985E5D5C7D44DC85794274FE25D0F79725B78F5B5DDD65A7813C09934450B9294651B96367E22012857B11485FDFF0E2E01E9607EC908B816B9F2E0494D%26nwait%3D0%26nnext%3D0%26tps%3D0.000000%26ttl%3D0%26ip%3Dzam.melon.com%26port%3D443; JSESSIONID=DA52BC72D99D8A539E9C893244EADC80; wcs_bt=s_585b06516861:1728845470',
        'Host': 'ticket.melon.com',
        'Referer': 'https://ticket.melon.com/reservation/popup/stepBlock.htm',
        'User-Agent': 'X'
    }

    response = requests.post(url,headers=header,data=body)
    return response.json()

def check_remaining_seats(seats: list) -> list:
    result = []
    
    for seat in seats:
        if seat['realSeatCntlk'] > 0:
            result.append(generate_message(seat))

    return result

def send_message(messages: list) -> None:
    slack_webhook_url = "https://hooks.slack.com/services/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"
    for message in messages:
        response = requests.post(slack_webhook_url, json={'text' : message})
   
def generate_message(seat: dict) -> str: 
    return seat['seatGradeName'] + ", " + seat['floorNo'] + seat['floorName'] + " " + seat['areaNo'] + seat['areaName'] + "에 잔여좌석 " + str(seat['realSeatCntlk']) + "개 발생! "

main()