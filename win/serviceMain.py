import win32serviceutil
import win32service
import win32event
import win32evtlogutil
import sys
sys.path.append(r'D:\Project\Tcp-DNS-proxy')
from tcpdns import ThreadedUDPRequestHandler, ThreadedUDPServer

import wmi 
def changeDNS(wmiService):
    colNicConfigs = wmiService.Win32_NetworkAdapterConfiguration(IPEnabled = True)
    for objNicConfig in colNicConfigs:
        arrDNSServers = ['127.0.0.1']
        objNicConfig.SetDNSServerSearchOrder(DNSServerSearchOrder = arrDNSServers)
def resetDNS(wmiService):
    colNicConfigs = wmiService.Win32_NetworkAdapterConfiguration(IPEnabled = True)
    for objNicConfig in colNicConfigs:
        returnValue = objNicConfig.SetDNSServerSearchOrder()
        returnValue = objNicConfig.EnableDHCP()

class DNSProxyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "tcpdns"
    _svc_display_name_ = "TCP DNS Proxy"
    _svc_description_ = "F**k GFW by TCP DNS Proxy"
    _svc_deps_ = ["EventLog"]

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        resetDNS(self.wmiService)
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.LocalServer.shutdown()
        sys.stdout.close()

    def SvcDoRun(self):
        import servicemanager

        win32evtlogutil.ReportEvent(self._svc_name_,
            servicemanager.PYS_SERVICE_STARTED,
            0, 
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            (self._svc_name_, ''))
        sys.stdout = open(r"d:\tcpLog.log",'w')
        self.LocalServer = ThreadedUDPServer(('127.0.0.1', 53), ThreadedUDPRequestHandler)
        self.wmiService = wmi.WMI ()
        changeDNS(self.wmiService)
        self.LocalServer.serve_forever()

        win32evtlogutil.ReportEvent(self._svc_name_,
            servicemanager.PYS_SERVICE_STOPPED,
            0,
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            (self._svc_name_, ''))   

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(DNSProxyService)