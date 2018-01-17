#! /usr/bin/python

import math
import time
import argparse
from Gnuplot import Gnuplot
from random import random

G=Gnuplot()
Long=100
Margen=4

def mod(v):
	return math.sqrt((v[0]**2)+(v[1]**2))

def fa(d):
	return (d**2)/(2*math.sqrt(Long))

def fr(d):
	return Long/d

def dist(u,v):
	return math.sqrt(((u[0]-v[0])**2)+((u[1]-v[1])**2))

def calc(u,v,n):
	d=dist(u,v)
	versor=[(u[0]-v[0])/d,(u[1]-v[1])/d]
	return (versor,d)

def sol_intersec(x,y):
	v=[y[0]-x[0],y[1]-x[1]]
	v=[v[0]*2/mod(v),v[1]*2/mod(v)]
	x=[x[0]+v[0],x[1]+v[1]]
	y=[y[0]-v[0],y[1]-v[1]]
	r=(x,y)
	return r

def dibujar_inicial(E,plano,tm=1):
	G('set title "Trabajo Practico Python:"')
	G(('set xrange [0:{0}]; set yrange [0:{0}]').format(Long+Margen))
	i=1
	for verice,coor in plano.items():
		G(('set object {0} circle center {1},{2} size 2 fc rgb "black"').format(i,coor[0]+Margen/2,coor[1]+Margen/2))
		i=i+1
	for e in E:
		coor1=plano[e[0]]
		coor2=plano[e[1]]
		coor1,coor2=sol_intersec(coor1,coor2)
		G(('set arrow nohead from {0},{1} to {2},{3}').format(coor1[0]+Margen/2,coor1[1]+Margen/2,coor2[0]+Margen/2,coor2[1]+Margen/2))
	G('plot NaN')
	time.sleep(tm)
	
def dibujar(E,plano,tm=0.5):
	G('reset')
	G('set title "Trabajo Practico Python:"')
	G(('set xrange [0:{0}]; set yrange [0:{0}]').format(Long+Margen))
	G('plot NaN')
	i=1
	for verice,coor in plano.items():
		G(('set object {0} circle center {1},{2} size 2 fc rgb "black"').format(i,coor[0]+Margen/2,coor[1]+Margen/2))
		i=i+1
	for e in E:
		coor1=plano[e[0]]
		coor2=plano[e[1]]
		coor1,coor2=sol_intersec(coor1,coor2)
		G(('set arrow nohead from {0},{1} to {2},{3}').format(coor1[0]+Margen/2,coor1[1]+Margen/2,coor2[0]+Margen/2,coor2[1]+Margen/2))
	G('replot')
	time.sleep(tm)

def setear():
	G('clear')
	G('reset')

def leer_grafo_stdin():
	n=int(raw_input("Ingrese cantidad de vertices\n"))
	V=[]
	E=[]
	for i in range(n):
		s=raw_input()
		V.append(s)
	print "Ingrese las aristas, al finalizar escriba 'EOF'"
	while True:
		s=raw_input()
		if s=="EOF":
			break
		s=s.split()
		if len(s)==1:
			print "Error al leer la ultima linea"
			continue
		if s[0] in V and s[1] in V:
			q=(s[0],s[1])
			w=(s[1],s[0])
			if q in E or w in E:
				print "Error, se ha ingresado una arista repetida"
			elif q!=w:
				E.append(q)
		else:
			print "Error al leer uno de los vertices"
	g=(V,E)
	return g

def leer_grafo_archivo(file_path):
	with open(file_path, "r") as f:
		V=[]
		E=[]
		n=int(f.readline())
		for i in range(n):
			s=f.readline()
			s=s[:-1]
			V.append(s)
		for line in f:
			line=line.split()
			if line[0] in V and line[1] in V:
				q=(line[0],line[1])
				w=(line[1],line[0])
				if q in E or w in E:
					print "Error, se ha ingresado una arista repetida"
				elif q!=w:
					E.append(q)
			else:
				print "Error al leer uno de los vertices"
		g=(V,E)
		return g

def inicializar(V,E):
	plano={}
	acumulador={}
	dic={}
	i=0
	for v in V:
		acumulador[v]=[0,0]
		dic[i]=v
		i+=1
		plano[v]=[abs((random()*1000*i)%Long),abs((random()*1000*i)%Long)]
	return (plano,acumulador,dic)

def posicionar(V,acumulador,pos,temp,f):
	for v in V:
		d=mod(acumulador[v]);
		if d!=0:
			acumulador[v][0]/=d
			acumulador[v][1]/=d
			d=min(d,temp)
			pos[v][0]+=acumulador[v][0]*d
			pos[v][1]+=acumulador[v][1]*d
			pos[v][0]=max(0,min(Long,pos[v][0]))
			pos[v][1]=max(0,min(Long,pos[v][1]))
		acumulador[v]=[0,0]
	return temp-f

def gravedad(V,acumulador,pos,n):
	c=[Long/2,Long/2]
	for v in V:
		u=[Long/2-pos[v][0],Long/2-pos[v][1]]
		d=mod(u)
		if d>(1/Long):
			versor=[u[0]/d,u[1]/d]
			acumulador[v][0]+=versor[0]/(Long*0.10)#10% de Long
			acumulador[v][1]+=versor[1]/(Long*0.10)#10% de Long

def atraer(E,acumulador,pos,n):
	for e in E:
		if pos[e[0]]!=pos[e[1]]:
			v,d=calc(pos[e[0]],pos[e[1]],n)
			if d>(1/Long):
				d=fa(d)/d
				v[0]*=d
				v[1]*=d
				acumulador[e[0]][0]-=v[0]
				acumulador[e[0]][1]-=v[1]
				acumulador[e[1]][0]+=v[0]
				acumulador[e[1]][1]+=v[1]

def repeler(V,acumulador,dic,pos,n):
	for i in range(n):
		for j in range(i+1,n):
			v,d=calc(pos[dic[i]],pos[dic[j]],n)
			if d>(1/Long):
				d=fr(d)/d
				v[0]*=d
				v[1]*=d
				acumulador[dic[i]][0]+=v[0]
				acumulador[dic[i]][1]+=v[1]
				acumulador[dic[j]][0]-=v[0]
				acumulador[dic[j]][1]-=v[1]

def fruchterman(grafo,it,v):
	V,E=grafo
	P,A,D=inicializar(V,E)
	n=len(V)
	T=float(Long)
	F=float(T/it)
	i=0
	if v==2:
		v=0
	else:
		v=it/(v-2)
	dibujar_inicial(E,P,1)
	while T>0:
		atraer(E,A,P,n)
		repeler(V,A,D,P,n)
		gravedad(V,A,P,n)
		T=posicionar(V,A,P,T,F)
		if i%v==0:
			dibujar(E,P)
		i=i+1
	dibujar(E,P,2)
	setear()
	return P

def main():
	
	parser=argparse.ArgumentParser()
	parser.add_argument('-c', '--Consola', action='store_true', help='Indica que el grafo sera leido desde terminal') 
	parser.add_argument('-a', '--Archivo', action='store_true', help='Indica que el grafo sera leido desde un archivo')
	parser.add_argument('-i','--Iters', type=int, help='Cantidad de iteraciones a efectuar', default=1000)
	parser.add_argument('-v','--Vistas', type=int, help='Cantidad de actualizaciones realizadas en pantalla', default=10)
	args = parser.parse_args()
	
	if args.Consola:
		grafo=leer_grafo_stdin()
	else:
		file_path=raw_input("Ingrese el nombre del archivo: ")
		print "Leyendo ",file_path
		grafo=leer_grafo_archivo(file_path);
	fruchterman(grafo,args.Iters,args.Vistas)

if __name__ == "__main__":
	main()
