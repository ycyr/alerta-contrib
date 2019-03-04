
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
#GEOIP_ACCESS_KEY = os.environ.get('GEOIP_ACCESS_KEY') or app.config.get('GEOIP_ACCESS_KEY', None)


class TriggerTicket(PluginBase):

    def pre_receive(self, alert):

#        ip_addr = alert.attributes['ip'].split(', ')[0]
#        LOG.debug("GeoIP lookup for IP: %s", ip_addr)

#        if 'ip' in alert.attributes:
#            url = '%s/%s?access_key=%s' % (EASYVISTA_URL, ip_addr, GEOIP_ACCESS_KEY)
#        else:
#            LOG.warning("IP address must be included as an alert attribute.")
#            raise RuntimeWarning("IP address must be included as an alert attribute.")
    
        data={'requests': [{'Catalog_Code': EASYVISTA_CATALOGID, 'Recipient.Last_name': 'Test', 'description': 'Test with Alerta'}]}
        r = requests.post(EASYVISTA_URL, auth=(EASYVISTA_USERNAME, EASYVISTA_PASSWORD), json=data) 
   #     r = requests.get(url, headers={'Content-type': 'application/json'}, timeout=2 )
        try:
            geoip_lookup = r.json()
            alert.attributes = {
                'geoip': geoip_lookup,
                'country': geoip_lookup['location'].get('country_flag_emoji')
            }
        except Exception as e:
            LOG.error("GeoIP lookup failed: %s" % str(e))
            raise RuntimeError("GeoIP lookup failed: %s" % str(e))

        return alert

    def post_receive(self, alert):
        return

    def status_change(self, alert, status, text):
        return
