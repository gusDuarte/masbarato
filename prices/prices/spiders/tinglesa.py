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

    def parse(self, response):
        for href in response.css("ul.menuprincipal > li > a.link::attr('href')"):
            cat_id = re.match(r'(.*=)(.*)', href.extract()).group(2)
            self.post(cat_id)
            yield

    def post(self, cat_id, pag=1):
        data = "idCategoria="+cat_id+"&buscadaDentro=&number=200&pagina=" + str(pag) + "&orden="
        url = 'http://www.tinglesa.com.uy/ajax/listado/listadosPaginadoSegunScroll.php'
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        print "DATA: " + data
        r = requests.post(url, data=data, headers=headers)
        try:
            res = r.json()
            found = res['cantidadArticulos']
            if found > 0:
                self.cantArt = self.cantArt + found
                print "         ==================================================="
                print "          Category-Id:" + cat_id + " (" + str(pag) + ") encontrados= " + str(res['cantidadArticulos'])
                print "          Total: " + str(self.cantArt)
                print "         ==================================================="
                pag = pag + 1
                self.post(cat_id, pag)
        except:
            print "Algo salio mal !"
            print sys.exc_info()[0]