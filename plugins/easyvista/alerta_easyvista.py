import logging
import requests
import json
import re
import os

from alerta.plugins import app
from alerta.plugins import PluginBase
from alerta.app import db

LOG = logging.getLogger('alerta.plugins.easyvista')


EASYVISTA_URL = os.environ.get('EASYVISTA_URL') or app.config['EASYVISTA_URL']
EASYVISTA_USERNAME = os.environ.get('EASYVISTA_USERNAME') or app.config['EASYVISTA_USERNAME']
EASYVISTA_PASSWORD = os.environ.get('EASYVISTA_PASSWORD') or app.config['EASYVISTA_PASSWORD']
EASYVISTA_CATALOGID = os.environ.get('EASYVISTA_CATALOGID') or app.config['EASYVISTA_CATALOGID']
EASYVISTA_CUSTOMERS = os.environ.get('EASYVISTA_CUSTOMERS') or app.config['EASYVISTA_CUSTOMERS']



class EasyVistaAlert(PluginBase):

    correlated = False

    def create_ticket(self, alert):
        data = {
                 "requests":[{
                               "Catalog_Code": EASYVISTA_CATALOGID ,
                               "description": "\
                                           ***Alerte générée depuis Alerta*** \n\n \
                                           Alerte: {} \n \
                                           Instance: {}\n \
                                           Informations supplémentaires: {} \n \
                                           ".format(alert.event, alert.resource if hasattr(alert, 'resource') else "N/A", alert.text if hasattr(alert, 'text') else "N/A")
                             }]
               }
        r = requests.post(EASYVISTA_URL, auth=(EASYVISTA_USERNAME, EASYVISTA_PASSWORD), json=data)
        LOG.info("HTTP Status Code: {} and Reason: {} ".format(r.status_code, r.reason))
        alert.attributes['ITSM'] = re.findall("(INC\d+)", r.json()["HREF"])[0]
        LOG.info("Ticket {} has been created in EasyVista".format(re.findall("(INC\d+)", r.json()["HREF"])[0]))

        return


    def retreive_ticket_status(self, alert):

        url = EASYVISTA_URL + '/' + str(alert.attributes['ITSM'])
        r = requests.get(url, auth=(EASYVISTA_USERNAME, EASYVISTA_PASSWORD)  )
        LOG.info("HTTP Status Code: {} and Reason: {} ".format(r.status_code, r.reason))
        ticket_status = r.json()["STATUS"]["STATUS_FR"]

        return ticket_status

   

    def pre_receive(self, alert):
         
        
        if db.is_correlated(alert) is True:
            self.correlated = True
            LOG.info("Correlated Alert: {}".format(self.correlated))
 
        return alert



    def post_receive(self, alert):

        LOG.info("Enhancing alert ITSM ")
        
        if  alert.customer != None and alert.customer in EASYVISTA_CUSTOMERS:

            LOG.info("{} in EASYVISTA_CUSTOMERS".format(alert.customer))
            LOG.info("Number of duplicates: {}".format(alert.duplicate_count))

            if  (alert.duplicate_count > 0 or self.correlated is True) and 'ITSM' in alert.attributes:

                LOG.info("Duplicated alert: Actual Ticket number: {}".format(alert.attributes['ITSM']))
                LOG.info("Ticket Status {}: {}".format(alert.attributes['ITSM'], self.retreive_ticket_status(alert)))

                if self.retreive_ticket_status(alert) =="Clôturé":

                    LOG.info("Creating a new ticket in Easyvista because {} has been closed".format(alert.attributes['ITSM']))

                    self.create_ticket(alert)
            else:

                LOG.info("Creating a new ticket in Easyvista")

                self.create_ticket(alert)

        else:
            LOG.info("Customer view not in EASYVISTA_CUSTOMERS")


        return alert

    def status_change(self, alert, status, text):
        return
