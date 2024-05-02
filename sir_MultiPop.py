"""Importação de Bibliotecas"""
import numpy as np
import random

from numpy.linalg import multi_dot

class population(object):
    """
    Classe que representa uma população
    """

    ALPHA = 0.05 #taxa de vacinação de suscetíveis

    def __init__(self, N, mu, betaIN, betaEX, gama, rho, alpha):
        self.N = N #número de indivíduos na população
        self.mu = mu #taxa de mortalidadee natalidade da população
        self.betaIN = betaIN #taxa de transmissão interna
        self.betaEX = betaEX #taxa de transmissão externa
        self.gama = gama #taxa de recuperação
        self.rho = rho #fração da vacinação
        self.alpha = alpha #taxa de vacinação de S

    def sis_equacoes(self, w, t, pop2):
        """
        Sistema de equações que modelam o SIR para a população
        """
        #TODO: Continuar a implementação do sistema de equações
        #S, I, R = w #valores de Suscetíves, Infectados e Recuperados

        W_pop = self.condicoes_iniciais() #Condições iniciais dessa população
        W_pop2 = pop2.condicoe_iniciais() #Condições iniciais da população externa

        N = self.N
        mu = self.mu
        betaIN = self.betaIN
        betaEX = self.betaEX
        gama = self.gama
        rho = self.rho
        alpha = self.alpha

        dwdt = [1, #Equação 1 
                beta*S*I/N - gama*I, 
                gama*I] #sistema com as três equações do modelo SIR

        return dwdt


     
    def intervalo_tempo(self):
        """
        Retorna um vetor com os intervalos de tempo para a simulação
        """
        ti = 0; #tempo inicial (dias)
        tf = 100; #tempo final (dias)
        tspan = np.linspace(ti, tf, 5*(tf-ti)) #500 pontos (5*100) para saída de dados

        t = [ti, tf, tspan] #vetor com as informações relativas ao tempo

        return t

    def condicoes_iniciais(self):
        """
        Retorna um vetor com as condições iniciais do problema
        """
        I0 = 1.0 #número de indíviduos infectados inicialmente
        S0 = self.N - I0 #número de indíviduos suscetíves inicialmente
        R0 = 0.0 #número de indíviduio recuperados inicialmente
        Icum0 = I0 #número inicial de infectados acumulados da população

        W0 = [S0, I0, R0, Icum0] #vetor com as condições iniciais

        return W0
    
