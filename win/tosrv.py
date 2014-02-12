from distutils.core import setup
import py2exe
TCP_DNS_Proxy = Target(
  description = "TCP DNS Proxy",
  modules=["serviceMain"],
  cmdline_style="pywin32")
setup(
    version = "",
    service=[TCP_DNS_Proxy]
    )