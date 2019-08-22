import os
import io
import json
import xlrd
import pycurl
import logging
import certifi
import smtplib
import traceback
from constant_host_unit import *
from email.mime.text import MIMEText
from email.MIMEImage import MIMEImage
from email.mime.multipart import MIMEMultipart

import sys  
sys.path.append("")

class email_details:
  def __init__(self):
    self.smtpserver = ""
    self.username = ""
    self.password = ""
    self.port = 0
    self.senders_list = ""
    self.receivers_list = ""

class tenantInfo:
   def __init__(self):
     self.tenant_url = ""
     self.tenant_token = ""
     self.name = ""
     self.threshold_host_units = ""
     self.allocated_host_units = ""
     self.threshold_dem_units = ""
     self.allocated_dem_units = ""

#------------------------------------------------------------------------------
# Author: Nikhil Goenka
# Function to initialize the email server
# Returns the smtp_server initialized 
#------------------------------------------------------------------------------
def initialize_email_server(logger, smtp_server_details):
  try:
    logger.info("In initialize_email_server")
    smtp_server = smtplib.SMTP(smtp_server_details.smtpserver,smtp_server_details.port )
    smtp_server.starttls()
    smtp_server.login(smtp_server_details.username, smtp_server_details.password)
    logger.info("Execution sucessfull: initialize_email_server")

  except Exception, e:
    traceback.print_exc()
    logger.error("Received exception while running initialize_email_server", str(e), exc_info = True)

  finally:
    return smtp_server

#------------------------------------------------------------------------------
# Author: Nikhil Goenka
# Function to send an email using the smtp_server initialized
# Returns: nothing 
#------------------------------------------------------------------------------

def send_email(logger, smtp_server, message, smtp_server_details):
  try:
    logger.info("In send_email")
    logger.debug ("send_email: smtp_server = %s", smtp_server)
    logger.debug ("send_email: message = %s", message)
    message["From"] = smtp_server_details.senders_list 
    message["To"] = smtp_server_details.receivers_list 
    smtp_server.sendmail(smtp_server_details.senders_list, (smtp_server_details.receivers_list).split(','), message.as_string())
    logger.info("Execution sucessfull: send_email")
  except Exception, e:
    traceback.print_exc()
    logger.error("Received exception while running send_email", str(e), exc_info = True) 

#------------------------------------------------------------------------------
# Author: Nikhil Goenka
# Function to make API call using the token defined in constant.py
# Returns the json object returned using the API call 
#------------------------------------------------------------------------------
def dtApiQuery(logger, endpoint, tenant_info, URL = ""):
  try: 
    if URL == "":
      URL = tenant_info.tenant_url
    logger.info("In dtApiQuery")
    logger.debug ("dtApiQuery: endpoint = %s", endpoint)
    buffer = io.BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, URL + endpoint)
    c.setopt(pycurl.CAINFO, certifi.where())
    c.setopt(c.HTTPHEADER, ['Authorization: Api-Token ' + str(tenant_info.tenant_token)] )
    c.setopt(pycurl.WRITEFUNCTION, buffer.write)
    c.perform()
    c.close()
    logger.info("Execution sucessfull: dtApiQuery")

  except Exception,e:
    traceback.print_exc()
    logger.error("Received exception while running dtApiQuery", str(e), exc_info = True) 

  finally:
    return(buffer.getvalue().decode('UTF-8'))

#------------------------------------------------------------------------------
# Author: Nikhil Goenka
# Function to create the html footer 
# Returns: nothing 
#------------------------------------------------------------------------------
def html_header(logger):
    try:
      logger.info("In html_header: ")
      html = """
      <html>
      <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      </head>
      <body bgcolor="#FFFFFF" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
      <center>
      <img src="cid:image1" class = "center" width:90%>
      </center>
      <br></br>
      <p> Hi Team, </p>
    """
    except Exception:
      traceback.print_exc()
      logger.error ("Received error while executing html_header %s", str(e))
    finally:
      return html
#------------------------------------------------------------------------------
# Author: Nikhil Goenka
# Function to create the html footer
# Accepts:
# msg: Message to indicate if the oneAgent was installed/uninstalled
# Returns: nothing 
#------------------------------------------------------------------------------

def html_body(logger, html, message):
    try:
      logger.info("In html_body: ")
      string = "<p>{msg}<p>\n"

      html = html + string.format(msg = message) + """ 
      <br></br>
      <br></br>
      <p>Thanks,</p>
      <p>Dynatrace Team</p>
      """
    except Exception:
      traceback.print_exc()
      logger.error ("Received error while executing html_body %s", str(e))
     
    finally:
      return html

#------------------------------------------------------------------------------
# Author: Nikhil Goenka
# Function to create the html footer
# Accepts: 
# html: html data to be written to in the email
# content: content is data written in the email (in a format that is supported by smtplib) 
# Returns: nothing 
#-----------------------------------------------------------------------------------------
def html_footer(logger, html, content):
    try:
      logger.info("In html_footer : ")
      logger.debug("In html_footer %s: ", content)

      html = html + """ 
      <img src="cid:image2">
       </center>
       </body>
       """

      content.attach(MIMEText(html, "html"))
      msgAlternative = MIMEMultipart('alternative')
      content.attach(msgAlternative)

      fp = open('images/Email_Template_01.jpg','rb')
      msgImage = MIMEImage(fp.read())
      fp.close()

      msgImage.add_header('Content-ID', '<image1>')
      content.attach(msgImage)

      fp = open('images/Email_Template_03.jpg','rb')
      msgImage = MIMEImage(fp.read())
      fp.close()

      msgImage.add_header('Content-ID', '<image2>')
      content.attach(msgImage)
     
    except Exception:
      traceback.print_exc()
      logger.error ("Received error while executing html_footer %s", str(e))
     
    finally:
      return content

def populate_consumption(logger, applications, syn = 0):
   try:
     logger.info("In populate_consumption")
     consumption = 0
 
     if syn == 0:
       apps = applications['metrics']['builtin:billing.apps.web.sessionsByApplication:fold(value)']['values']
     elif syn == 1:
       apps = applications['metrics']['builtin:billing.synthetic.actions:fold(value)']['values']
     elif syn == 2:
       apps = applications['metrics']['builtin:billing.synthetic.requests:fold(value)']['values']

     for billing in apps:
       dimensions = billing['dimensions']
       if syn == 0:
         if dimensions[1] == "Billed":
           consumption = consumption + billing['value']
       elif syn == 1:
           consumption = consumption + billing['value']
       elif syn == 2:
           consumption = consumption + billing['value']

   except Exception, e:
     traceback.print_exc()
     logger.fatal("Encountered error while executing calc_dem_units = %s", str(e), exc_info = True)

   finally:
     return consumption

def calc_dem_units(logger, tenant_info):
    try:
      logger.info("In calc_dem_units")
      logger.debug("tenant_info = %s", tenant_info)
      
      url = ""
      url = (tenant_info.tenant_url).replace("v1","v2")
      
      dem_units = 0
      applicationIO = dtApiQuery(logger, APP_BILLING_API, tenant_info, url)
      applications = json.loads(applicationIO)
      app_session = populate_consumption(logger, applications, 0)
      dem_units = dem_units + (app_session * 0.25)

      applicationIO = dtApiQuery(logger, SYNC_BILLING_API, tenant_info, url)
      applications = json.loads(applicationIO)
      syn_session = populate_consumption(logger, applications, 1)
      dem_units = dem_units + (syn_session * 1)
    
      applicationIO = dtApiQuery(logger, HTTP_BILLING_API, tenant_info, url)
      applications = json.loads(applicationIO)
      http_session = populate_consumption(logger, applications, 2)
      dem_units = dem_units + (syn_session * 0.1)
      
    except Exception, e:
      traceback.print_exc()
      logger.fatal("Encountered error while executing calc_dem_units = %s", str(e), exc_info = True)
   
    finally:
      return dem_units
#------------------------------------------------------------------------
# Author: Nikhil Goenka
# Function to call API and populate the excel file
#------------------------------------------------------------------------
def func(logger, totalHostUnits, tenant_info, smtp_server):
  try:
    logger.info("In func")
    logger.debug("func: totalHostUnits = %s", totalHostUnits)  
    logger.debug("func: smtp_server = %s", smtp_server)

    dem_threshold = 0
    host_threshold = 0

    content = MIMEMultipart('related')
    html = html_header(logger)

    hostsIO = dtApiQuery(logger, API_CALL, tenant_info)
    hosts = json.loads(hostsIO)

    for host in hosts:
      totalHostUnits = totalHostUnits + float(host['consumedHostUnits'])

    dem_units = calc_dem_units(logger, tenant_info)
    
    #Host Unit threshold breached
    if(float(totalHostUnits) > (float(tenant_info.threshold_host_units * tenant_info.allocated_host_units)/100)):
      content["Subject"] = "ALERT: Host Units Consumption "
      msg = "This is to bring to your notice that the current Host Unit Consumption " + str(float(totalHostUnits)) + "  has exceeded the configured threshold of " + str(tenant_info.allocated_host_units)
      host_threshold = 1
    
    #DEM Unit threshold breached
    if(float(dem_units) > (float(tenant_info.threshold_dem_units * tenant_info.allocated_dem_units)/100)):
      content["Subject"] = "ALERT: DEM Units Consumption "
      msg = "This is to bring to your notice that the current DEM Unit Consumption " + str(float(dem_units)) + "  has exceeded the configured threshold of " + str(tenant_info.allocated_dem_units)
      dem_threshold = 1

    # Both breached
    if dem_threshold == 1 and host_threshold == 1: 
      content["Subject"] = "ALERT: Host and DEM Units Consumption "
      msg = "This is to bring to your notice that the current DEM Unit Consumption " + str(float(dem_units)) + "  has exceeded the configured threshold of " + str(tenant_info.threshold_dem_units) + "%. Also the current Host Unit Consumption " + str(float(totalHostUnits)) + " has exceeded the configured threshold of " + str(tenant_info.threshold_host_units) + "%."

    if dem_threshold == 1 or host_threshold == 1:
      html = html_body(logger, html, msg)
      content = html_footer(logger, html, content)
      send_email(logger, smtp_server, content, smtp_server_details)
 
    logger.info("Successful execution: func")
    
  except Exception,e:
    traceback.print_exc()
    logger.fatal("Received exception while running func", str(e), exc_info=True)

#------------------------------------------------------------------------
# Author: Nikhil Goenka
# filename: the config file which the user would configure
#------------------------------------------------------------------------
def parse_config(filename):
  try:
    stream = open(filename)
    data = json.load(stream)
  except Exception:
    traceback.print_exc()
    print "Exception encountered in parse_config function : %s ", str(e)
  finally:
    return data

#------------------------------------------------------------------------
# Author: Nikhil Goenka
# smtp_server_details: email_details object that will contain information about the smtp server
#------------------------------------------------------------------------
def populate_smtp_variable(data, smtp_server_details):
  try:
    smtp_server = data['email-details']
    smtp_server_details.username = smtp_server['username']
    smtp_server_details.password = smtp_server['password'] 
    smtp_server_details.smtpserver = smtp_server['server']
    smtp_server_details.port = int(smtp_server['port'])
    smtp_server_details.senders_list = smtp_server['senders-list'] 
    smtp_server_details.receivers_list = smtp_server['receiver-list']

  except Exception, e:
    traceback.print_exc()
    print "Exception encountered while executing populate_smtp_variable %s ", str(e)
  finally:
    return smtp_server_details

#------------------------------------------------------------------------
# Author: Nikhil Goenka
# Function to call API and populate the excel file
#------------------------------------------------------------------------
def populate_tenant_details(logger, tenant, tenant_info):
  try:
    logger.info("In populate_tenant_details")
    logger.info("In populate_tenant_details %s ", tenant)

    tenant_info.tenant_url = tenant['tenant-URL'] 
    tenant_info.tenant_token = tenant['API-token']
    tenant_info.name = tenant['tenant-name']
    tenant_info.allocated_host_units = float(tenant['allocated-host-units'])
    tenant_info.threshold_host_units = float(tenant['threshold-host-units'])
    tenant_info.allocated_dem_units = float(tenant['allocated-dem-units'])
    tenant_info.threshold_dem_units = float(tenant['threshold-dem-units'])
  except Exception, e:
    traceback.print_exc()
    print "Exception encountered while executing populate_tenant_details %s ", str(e)
  finally:
    return tenant_info 

#------------------------------------------------------------------------
# Author: Nikhil Goenka
# Function to call API and populate the excel file
#------------------------------------------------------------------------

#tmp_hostName: list with the current host name 
#tmp_hostUnits: list with the hostUnits
#totalHostUnits: total current host units

if __name__ == "__main__":
  try:
    totalHostUnits = 0
    filename = "config_threshold.json"
    tenant_info = tenantInfo()

    data = parse_config(filename)
    smtp_server_details = email_details()
    smtp_server_details = populate_smtp_variable(data, smtp_server_details)

    logging.basicConfig(filename=data['log_file'],
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)
    logger = logging.getLogger()
    smtp_server = initialize_email_server(logger, smtp_server_details)
    tenant_info = populate_tenant_details(logger, data['tenant-details'], tenant_info)
    func(logger, totalHostUnits, tenant_info, smtp_server)

  except Exception, e:
    traceback.print_exc()
    logger.error("Received exception while running func", str(e))
  
  finally:
    smtp_server.close()
