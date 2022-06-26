string = input()
ss = string.split('.')
def judge(ss):
    if len(ss) == 4: # ipv4
        for s in ss:
            if s[0] == '0' or int(s) < 0 or int(s) > 255:
                print('Neither')
                return
        print('IPv4')
    elif len(ss) == 1:
        ss = ss[0].split(":")
        if len(ss) != 8:
            print('Neither')
        else:
            for s in ss:
                if len(s) > 4 or len(s) == 0:
                    print('Neither')
                    break
                if set(s) == set('0') and len(s) > 1:
                    print('Neither')
                    break
            else:
                print('IPv6')
judge(ss)