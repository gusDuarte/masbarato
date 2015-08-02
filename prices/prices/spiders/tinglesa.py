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
            url = response.urljoin(href.extract())
            print "Category-0:  url=" + url
            yield scrapy.Request(url, callback=self.parse_categories_level_1)

    def parse_categories_level_1(self, response):
        cant = len(response.css("table.categorias_niveles > tr > td.nivel1 > ul > li"))
        print "Category-1:   url=" + response.url + ", " + str(cant)
        for cat in response.css("table.categorias_niveles > tr > td.nivel1 > ul > li"):
            cat_name = cat.xpath('./text()').extract()[0]
            res = cat.xpath('@onclick').re(r'(categorias_segundoPaso\(this.*\')(.*)(\')')
            if len(res) > 0:
                item={'cat_name': cat_name}
                cat_id = res[1]
                url = response.urljoin("/ajax/categorias/paso2.php?idCategoria=" + cat_id)
                print "         Category-1: " + cat_name + ", " + cat_id + ", " + url
                req = scrapy.Request(url, callback=self.parse_categories_level_2)
                req.meta['item'] = item
                yield req



    def parse_categories_level_2(self, response):
        cant = len(response.css("ul > li"))
        print "Category-2:   url= " + response.url + ", cant= " + str(cant)

        for cat in response.css("ul > li"):
            cat_name = cat.xpath('./text()').extract()[0]
            res = cat.xpath('@onclick').re(r'(categorias_tercerPaso\(this.*\')(.*)(\')')
            if len(res) > 0:
                item={'cat_name': cat_name}
                cat_id =  res[1]
                url = response.urljoin("/ajax/categorias/paso3.php?idCategoria=" + cat_id)
                print "         Category-2: " + cat_name + ", " + cat_id + ", " + url
                req = scrapy.Request(url, callback=self.parse_categories_level_3)
                req.meta['item'] = item
                yield req
        if cant == 0:
            cat_id = re.match(r'(.*=)(.*)',response.url).group(2)
            data = "idCategoria="+cat_id+"&buscadaDentro=&number=1000&pagina=1&orden="
            url = 'http://www.tinglesa.com.uy/ajax/listado/listadosPaginadoSegunScroll.php'
            headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
            r = requests.post(url, data=data, headers=headers)
            try:
                res = r.json()
                self.cantArt = self.cantArt + res['cantidadArticulos']
                item = response.meta['item']
                print "         ==================================================="
                print "          Category-2 "+ item['cat_name'] +": encontrados: " + str(res['cantidadArticulos'])
                print "          Total: " + str(self.cantArt)
                print "         ==================================================="
            except:
                print sys.exc_info()[0]

    def parse_categories_level_3(self, response):
        cant = len(response.css("ul > li"))
        print "Category-3:   url= " + response.url + ", cant= " + str(cant)

        for cat in response.css("ul > li"):
            cat_name = cat.xpath('./text()').extract()[0]
            res = cat.xpath('@onclick').re(r'(categorias_cuartoPaso\(this.*\')(.*)(\')')
            if len(res) > 0:
                item={'cat_name': cat_name}
                cat_id =  res[1]
                url = response.urljoin("/ajax/categorias/paso4.php?idCategoria=" + cat_id)
                print "         Category-3: " + cat_name + ", " + cat_id + ", " + url
                req = scrapy.Request(url, callback=self.parse_categories_level_4)
                req.meta['item'] = item
                yield req
        if cant == 0:
            cat_id = re.match(r'(.*=)(.*)',response.url).group(2)
            data="idCategoria="+cat_id+"&buscadaDentro=&number=1000&pagina=1&orden="
            url = 'http://www.tinglesa.com.uy/ajax/listado/listadosPaginadoSegunScroll.php'
            headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
            r = requests.post(url, data=data, headers=headers)
            try:
                res = r.json()
                self.cantArt = self.cantArt + res['cantidadArticulos']
                item = response.meta['item']
                print "         ==================================================="
                print "          Category-3 "+ item['cat_name'] +": encontrados: " + str(res['cantidadArticulos'])
                print "          Total: " + str(self.cantArt)
                print "         ==================================================="
            except:
                print sys.exc_info()[0]

    def parse_categories_level_4(self, response):

        cant = len(response.css("ul > li"))
        print "Category-4:   url= " + response.url + ", cant= " + str(cant)

        for cat in response.css("ul > li"):
            cat_name = cat.xpath('./text()').extract()[0]
            cat_id = cat.xpath('@onclick').re(r'(categorias_cuartoPaso\(this,\')(.*)(\'\))')[1]
            data="idCategoria="+cat_id+"&buscadaDentro=&number=1000&pagina=1&orden="
            url = 'http://www.tinglesa.com.uy/ajax/listado/listadosPaginadoSegunScroll.php'
            headers  = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
            r = requests.post(url, data=data, headers=headers)
            try:
                res = r.json()
                self.cantArt = self.cantArt + res['cantidadArticulos']
                item = response.meta['item']
                print "         ==================================================="
                print "          Category-4 "+ item['cat_name'] +": encontrados: " + str(res['cantidadArticulos'])
                print "          Total: " + str(self.cantArt)
                print "         ==================================================="
            except:
                print sys.exc_info()[0]
