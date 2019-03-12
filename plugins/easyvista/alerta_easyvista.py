import logging
import requests
import json
import re
import os

from alerta.plugins import app
from alerta.plugins import PluginBase

LOG = logging.getLogger('alerta.plugins.easyvista')


EASYVISTA_URL = os.environ.get('EASYVISTA_URL') or app.config['EASYVISTA_URL']
EASYVISTA_USERNAME = os.environ.get('EASYVISTA_USERNAME') or app.config['EASYVISTA_USERNAME']
EASYVISTA_PASSWORD = os.environ.get('EASYVISTA_PASSWORD') or app.config['EASYVISTA_PASSWORD']
EASYVISTA_CATALOGID = os.environ.get('EASYVISTA_CATALOGID') or app.config['EASYVISTA_CATALOGID']
EASYVISTA_CUSTOMERS = os.environ.get('EASYVISTA_CUSTOMERS') or app.config['EASYVISTA_CUSTOMERS']

data = {"requests":[{"Catalog_Code": EASYVISTA_CATALOGID ,"Recipient.Last_name":"Test","description":"Bravo Alerta"}]}


class EasyVistaAlert(PluginBase):

    def pre_receive(self, alert):

        return alert

    def post_receive(self, alert):

        LOG.info("Enhancing alert ITSM ")


        if  alert.customer != None and alert.customer in EASYVISTA_CUSTOMERS:
            LOG.info("BON CUSTOMER")
            LOG.info("Nombre de duplicas: {}".format(alert.duplicate_count))
            if  alert.duplicate_count > 0:
                LOG.info("Alerte dupliquée: No Ticket actuel: {}".format(alert.attributes['ITSM']))
                url = EASYVISTA_URL +'/' + str(alert.attributes['ITSM'])
                r = requests.get(url, auth=(EASYVISTA_USERNAME, EASYVISTA_PASSWORD)  )
                LOG.info(r.status_code)
                LOG.info(r.reason)
                ticket_status = r.json()["STATUS"]["STATUS_FR"]
                LOG.info(ticket_status)

                if r.json()["STATUS"]["STATUS_FR"] =="Clôturé":
                    LOG.info("Ouverture d'un nouveau ticket EASYVISTA car le ticket {} a été clôturé".format(alert.attributes['ITSM']))
                    r = requests.post( EASYVISTA_URL, auth=(EASYVISTA_USERNAME, EASYVISTA_PASSWORD), json=data)
                    LOG.info(r.status_code)
                    LOG.info(r.reason)
                    LOG.info(r.json())
                    alert.attributes['ITSM'] = re.findall("(INC\d+)", r.json()["HREF"])[0]
                    LOG.info("Le ticket {} a été crée dans EasyVista".format(re.findall("(INC\d+)", r.json()["HREF"])[0]))
            else:
                LOG.info("Ouverture d'un nouveau ticket EASYVISTA")

                r = requests.post( EASYVISTA_URL, auth=(EASYVISTA_USERNAME, EASYVISTA_PASSWORD), json=data)
                LOG.info(r.status_code)
                LOG.info(r.reason)
                LOG.info(r.json())
                alert.attributes['ITSM'] = re.findall("(INC\d+)", r.json()["HREF"])[0]
                LOG.info("Le ticket {} a été crée dans EasyVista".format(re.findall("(INC\d+)", r.json()["HREF"])[0]))

        else:
            LOG.info("PAS BON CUSTOMER")


        return alert

    def status_change(self, alert, status, text):
        return
