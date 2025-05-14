import subprocess
import time

if __name__ == '__main__':
    filename = '/home/vinayj/startup_scraper/newstartups/crunchlinks.txt'
    f = open(filename, 'r')
    txt = f.read()
    f.close()
    if str(txt) == "0":
        f = open(filename, 'w')
        f.write("1")
        f.close()
        try:
            print("Starting urlrunner")
            subprocess.call(['sh', '/home/vinayj/startup_scraper/newstartups/urls.sh'])
            print("Stopping urlrunner")
        except Exception as e:
            print(e)
            pass
        f = open(filename, 'w')
        f.write("0")
        f.close()
    else:
        print(" Another process is already running")

