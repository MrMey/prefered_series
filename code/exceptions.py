# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 16:45:35 2017

@author: Mr_Mey
"""

class DataBaseError(Exception):
    """Exception levée dans un certain contexte… qui reste à définir"""
    def __init__(self, message):
        """On se contente de stocker le message d'erreur"""
        self.message = message
        
    def __str__(self):
        """On renvoie le message"""
        return self.message