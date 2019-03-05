#!/usr/bin/python3


import logging
import os
import requests
import json
import re

try:
    from alerta.plugins import app  # alerta >= 5.0
except ImportError:
    from alerta.app import app  # alerta < 5.0
from alerta.plugins import PluginBase

LOG = logging.getLogger('alerta.plugins.easyvista')

EASYVISTA_URL = os.environ.get('EASYVISTA_URL') or app.config.get('EASYVISTA_URL', None)
EASYVISTA_USERNAME = os.environ.get('EASYVISTA_USERNAME') or app.config.get('EASYVISTA_USERNAME', None)
EASYVISTA_PASSWORD = os.environ.get('EASYVISTA_PASSWORD') or app.config.get('EASYVISTA_PASSWORD', None)
EASYVISTA_CATALOGID = os.environ.get('EASYVISTA_CATALOGID') or app.config.get('EASYVISTA_CATALOGID', None)
EASYVISTA_CUSTOMERS = os.environ.get('EASYVISTA_CUSTORMERS') or app.config.get('EASYVISTA_CUSTOMERS', None)

class TriggerTicket(PluginBase):

    def pre_receive(self, alert):

    	if alert.customer in EASYVISTA_CUSTORMERS:
        	if not alert.is_duplicate():
        		   if not alert.attributes['easyvista_num']:
        	   		        data={'requests': [{'Catalog_Code': EASYVISTA_CATALOGID, 'Recipient.Last_name': 'Test', 'description': 'Test with Alerta'}]}
                    	    try: 
                        		r = requests.post(EASYVISTA_URL, auth=(EASYVISTA_USERNAME, EASYVISTA_PASSWORD), json=data) 
                        		ticket_response = r.json
                        		ticket_num_list = re.findall("(INC\d+)", ticket_response["HREF"])
                        		alert.attributes = {
                            		   'easyvista_num' : ticket_num_list[0]
                        		}

      						except Exception as e:
      							LOG.error("Ticket Creation failed: %s" % str(e))
            					raise RuntimeError("Ticket Creation lookup failed: %s" % str(e))

        return alert

    def post_receive(self, alert):
        return

    def status_change(self, alert, status, text):
        return
