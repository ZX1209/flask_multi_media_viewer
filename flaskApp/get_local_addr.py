import socket


def get_lan_ip():
    """
    查询本机ip地址
    :return: ip
    """
    ipstr = "no net?"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ipstr = s.getsockname()[0]
    except:
        import subprocess

        cmdstr = 'ifconfig | grep -E "inet[^6]"'
        proc = subprocess.Popen(
            cmdstr, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        results = proc.communicate()
        ipstr = str(results[0], encoding="utf-8")
    finally:
        s.close()

    return ipstr
