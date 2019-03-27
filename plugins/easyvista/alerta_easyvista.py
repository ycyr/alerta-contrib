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

data = {"requests":[{"Catalog_Code": EASYVISTA_CATALOGID ,"Recipient.Last_name":"Test","description":"Alerte générée depuis Alerta"}]}


class EasyVistaAlert(PluginBase):

    correlated = False

    def create_ticket(self, alert):

        r = requests.post(EASYVISTA_URL, auth=(EASYVISTA_USERNAME, EASYVISTA_PASSWORD), json=data)
        LOG.info("Réponse HTTP: {} et Explication: {} ".format(r.status_code, r.reason))
        alert.attributes['ITSM'] = re.findall("(INC\d+)", r.json()["HREF"])[0]
        LOG.info("Le ticket {} a été crée dans EasyVista".format(re.findall("(INC\d+)", r.json()["HREF"])[0]))

        return


    def retreive_ticket_status(self, alert):

        url = EASYVISTA_URL + '/' + str(alert.attributes['ITSM'])
        r = requests.get(url, auth=(EASYVISTA_USERNAME, EASYVISTA_PASSWORD)  )
        LOG.info("Réponse HTTP: {} et Explication: {} ".format(r.status_code, r.reason))
        ticket_status = r.json()["STATUS"]["STATUS_FR"]

        return ticket_status


    def pre_receive(self, alert):
         
        
        if db.is_correlated(alert) is True:
            self.correlated = True
            LOG.info("Alerte Corrollée PRE: {}".format(self.correlated))
 
        return alert



    def post_receive(self, alert):

        LOG.info("Enhancing alert ITSM ")
        
        
        LOG.info("Function POST: {}".format(self.correlated))
        if  alert.customer != None and alert.customer in EASYVISTA_CUSTOMERS:

            LOG.info("BON CUSTOMER")
            LOG.info("Nombre de duplicas: {}".format(alert.duplicate_count))

            if  alert.duplicate_count > 0 or self.correlated is True:

                LOG.info("Alerte Corrollée POST: {}".format(self.correlated))
                LOG.info("Alerte dupliquée: No Ticket actuel: {}".format(alert.attributes['ITSM']))
                LOG.info("Status du ticket {}: {}".format(alert.attributes['ITSM'], self.retreive_ticket_status(alert)))

                if self.retreive_ticket_status(alert) =="Clôturé":

                    LOG.info("Ouverture d'un nouveau ticket EASYVISTA car le ticket {} a été clôturé".format(alert.attributes['ITSM']))

                    self.create_ticket(alert)
            else:

                LOG.info("Ouverture d'un nouveau ticket EASYVISTA")

                self.create_ticket(alert)

        else:
            LOG.info("PAS BON CUSTOMER")


        return alert

    def status_change(self, alert, status, text):
        return
