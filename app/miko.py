from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException,\
    NetMikoAuthenticationException


def setup():
    # Not yet in use...
    from datetime import datetime
    run_time = datetime.now().strftime('%Y-%m-%d_%H-%M')

    ios_device = {'device_type': 'cisco_ios'}
    username = user
    pass


def filesetup(filename):
    import os
    # refers to application_top:
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    fullfile = os.path.join(APP_ROOT, filename + '.txt')
    return fullfile


def dochangepass(user, oldPass, newPass, oldENPass, newENPass):
    ios_device = {'device_type': 'cisco_ios'}

    username = user
    userPass = [oldPass, newPass]
    enablePass = [oldENPass, newENPass]

    ios_device['username'] = username  # current username
    ios_device['password'] = userPass[0]  # old user_pass
    ios_device['secret'] = enablePass[0]  # old enable_pass

    config_commands = ['username ' + username + ' password ' + userPass[1],
                       'enable secret ' + enablePass[1],
                       'do wr']

    devices = filesetup("devices")

    with open(devices) as fp:
        for line in fp:
            line = line[:-1]
            ios_device['ip'] = line
            print(":::::::::::::" + line + ":::::::::::::")
            try:
                net_connect = ConnectHandler(**ios_device)
                net_connect.enable()
                output = net_connect.send_config_set(config_commands)
                net_connect.disconnect()
                print(output)
            except NetMikoAuthenticationException as e:
                z = e
                print(z)
            except NetMikoTimeoutException as e:
                z = e
                print(z)
                print("Device is unreachable.")
            except Exception as e:
                z = e
                print("\nOops! A general error occurred, here's the message:")
                print(z)


def doconfthrow(user, user_pass, enPass, confmode):
    ios_device = {'device_type': 'cisco_ios'}
    username = user
    userPass = user_pass

    config_mode = confmode

    if config_mode == "conft":
        enablePass = enPass
        ios_device['secret'] = enablePass
    elif config_mode == "user":
        pass

    ios_device['username'] = username
    ios_device['password'] = userPass
    config_commands = []

    from datetime import datetime
    run_time = datetime.now().strftime('%Y-%m-%d_%H-%M')
    logfile = './app/cmds-' + run_time + '.log'
    print("Beginning log to - " + logfile)

    def logme(output):
        f1 = open(logfile, 'a')
        f1.write(output + "\n")
        print(output)

    commands = filesetup("commands")

    with open(commands) as fp:
        for line in fp:
            line = line[:-1]
            config_commands.append(line)

    devices = filesetup("devices")

    with open(devices) as fp:
        for line in fp:
            line = line[:-1]
            ios_device['ip'] = line
            logme("\n:::::::::::::" + line + ":::::::::::::")
            try:
                net_connect = ConnectHandler(**ios_device)
                if config_mode == "conft":
                    net_connect.enable()
                    output = net_connect.send_config_set(config_commands)
                    logme(output)
                elif config_mode == "user":
                    for cmd in config_commands:
                        logme(cmd + ":")
                        output = net_connect.send_command(cmd)
                        logme(output)
                net_connect.disconnect()
            except NetMikoAuthenticationException as e:
                z = str(e)
                logme(z)
            except NetMikoTimeoutException as e:
                z = str(e)
                logme(z)
                logme("Device is unreachable.")
            except Exception as e:
                z = str(e)
                logme("\nOops! A general error occurred, here's the message:")
                logme(z)
