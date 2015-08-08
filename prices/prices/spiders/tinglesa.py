# -*- coding: utf-8 -*-
import scrapy
import re
import requests
import sys


class TinglesaSpider(scrapy.Spider):
    name = "tinglesa"
    allowed_domains = ["tinglesa.com.uy"]
    start_urls = (
        'http://www.tinglesa.com.uy',
    )

    def __init__(self):
        self.cantArt=0
        self.log = self.logger
        self.log.info("tinglesa spider start ...")
        self.art = list()

    def parse(self, response):
        for href in response.css("ul.menuprincipal > li > a.link::attr('href')"):
            cat_id = re.match(r'(.*=)(.*)', href.extract()).group(2)
            self.post(cat_id)
            yield

    def post(self, cat_id, pag=1):
        data = "idCategoria="+cat_id+"&buscadaDentro=&number=100&pagina=" + str(pag) + "&orden="
        url = 'http://www.tinglesa.com.uy/ajax/listado/listadosPaginadoSegunScroll.php'
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        self.log.debug("DATA: " + data)
        try:
            r = requests.post(url, data=data, headers=headers)
        except requests.exceptions.Timeout:
            self.log.warning("Try again ...")
            self.post(cat_id, pag)
        except request.exceptions.RequestException as e:
            self.log.error(e)
            return 
        try:     
            res = r.json()
            found = res['cantidadArticulos']
            total = res['resultados']
            if pag == 1:
                self.art.append({"id": cat_id, "total": total, "parcial": 0})
            if found > 0:
                self.art[-1]['parcial'] = found + self.art[-1]['parcial']
                self.cantArt = self.cantArt + found
                self.log.info( "         ===================================================")
                self.log.info( "          Id: " + cat_id + ", pag: " + str(pag) + ", encontrados= " + str(found))
                self.log.info( "          Parcial: " + str(self.art[-1]['parcial']) + "/"+str(total) + "\n") 
                self.log.info( "          Total: " + str(self.cantArt)) 
                self.log.info( "         ===================================================")
                pag = pag + 1
                self.post(cat_id, pag)
            else:
                self.log.info("         ************ NO hay mas articulos ***********")
        except Exception as e:
            self.log.error(e)
            self.log.debug("-------------------------")
            self.log.debug(r) 
            self.log.debug("-------------------------")
            
            t=[x for x in self.art if x['id']==cat_id]
            if len(t) > 0:
                if self.cantArt < t[0]['total']:
                    self.log.warning("Try again ...")
                    self.post(cat_id, pag)
                else:
                    self.log.info("         ************ NO hay mas articulos ***********")
