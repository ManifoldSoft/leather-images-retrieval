# -*- coding: utf-8 -*-

from __future__ import print_function

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage as nd

from skimage import data
from skimage.util import img_as_float
from skimage.filters import gabor_kernel

from tools.imtools import get_imlist
from skimage import io

# import PIL and pylab for plotting        
from PIL import Image
from pylab import *

import time
import os

import pickle

import cherrypy
import urllib
import numpy

"""
This is the image search demo.
"""


class SearchDemo:

    def __init__(self):
        # load list of images
        self.path = './corel1k/'
        self.imlist = [os.path.join(self.path,f) for f in os.listdir(self.path) if f.endswith('.jpg')]
        self.nbr_images = len(self.imlist)
        self.ndx = range(self.nbr_images)

        # set max number of results to show
        self.inputFeature = open('gaborFeature.pkl', 'rb')
        self.feat = pickle.load(self.inputFeature)
        self.inputFeature.close()
        self.maxres = 20

        # header and footer html
        self.header = """
            <!doctype html>
            <head>
            <title>以图搜图</title>
            <link rel="stylesheet" href="/bootstrap/css/bootstrap.min.css">
            <link rel="stylesheet" href="style.css">
            <script src='http://cdn.bootcss.com/jquery/1.11.2/jquery.min.js'></script>
            <script src='/bootstrap/js/bootstrap.min.js'></script>
            </head>
            <body>
            """
        self.footer = """
            </html>
            """

    @cherrypy.expose
    def shutdown(self):  
        cherrypy.engine.exit()

    def index(self, query=None):

        html = self.header
        html += """
                <div class="jumbotron">
                    <div class="row">
                        <div class="col-lg-4 col-lg-offset-4">
                            <div class="input-group input-group-lg">
                                <input type="text" class="form-control" placeholder="以图搜图" name="srch-term" id="srch-term">
                                    <div class="input-group-btn">
                                        <button class="btn btn-gray" type="submit"><i class="glyphicon glyphicon-search"></i></button>
                                    </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="randButton">
                    <div class="row">
                        <button class="btn btn-default center-block btn-lg btn-success" type="button"><a href='?query='>随机图片</a></button>
                        <!--<button class="btn btn-default btn-lg btn-warning" type="button"><a id="shutdown"; href="./shutdown">关闭服务器</a></button>-->
                    </div>
                </div>
            """

        if query:
            #print query
            queryID = self.imlist.index(query)
            queryVec = self.feat[queryID]

            #score = numpy.zeros(shape=(self.imNum, 1))

            dis = []
            for i in range(self.feat.shape[0]):
                error = np.sum((queryVec - self.feat[i, :])**2)
                dis = dis+[error]
            rank_ID = sorted(range(len(dis)), key=lambda k: dis[k])

            #rank_ID = numpy.argsort(score)[::-1]

            #rank_score = score[rank_ID] 

            imlist = [self.imlist[index] for index in rank_ID[0:self.maxres]]

            for imname in imlist:
                html += "<div class='col-xs-6 col-sm-4 col-md-2 marginDown' >"
                #html += "<div class='col-sm-6 col-md-3'>"

                html += "<a href='?query="+imname+"' class='thumbnail'>"
                #html += "<a href='?query="+imname+"'>"

                html += "<img class='img-responsive' style='max-height:220px' src='"+imname+"'  />"
                #html += "<img src='"+imname+"' width='200px' height='200px' />"
                html += "</a>"
                html += "</div>"
        else:
            # show random selection if no query
            numpy.random.shuffle(self.ndx)
            for i in self.ndx[:self.maxres]:
                imname = self.imlist[i]
                html += "<div class='col-xs-6 col-sm-4 col-md-2 marginDown' >"
                #html += "<div class='col-sm-6 col-md-3'>"

                html += "<a href='?query="+imname+"' class='thumbnail'>"
                #html += "<a href='?query="+imname+"'>"

                html += "<img class='img-responsive' style='max-height:200px' src='"+imname+"'  />"
                #html += "<img src='"+imname+"' width='200px' height='200px' />"
                html += "</a>"
                html += "</div>"
                html += "</body>"
        html += self.footer
        html += """
                <footer>
                <p class='linkings'><a href='http://yongyuan.name/'>Created by Yong Yuan</a></p>
                </footer>
                """
        return html

    index.exposed = True

cherrypy.quickstart(SearchDemo(), '/', config=os.path.join(os.path.dirname(__file__), 'service.conf'))
