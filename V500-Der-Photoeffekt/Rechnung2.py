import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from uncertainties import ufloat
from table import(
	make_table,
	make_SI,
	write)

# Spannungen und Ströme einlesen
spannung_orange, orange = np.genfromtxt('Daten1.txt', unpack=True)
spannung, rot, grun, lila, blau, uv = np.genfromtxt('Daten2.txt', unpack=True)
matrix=np.array([rot, grun, lila, blau, uv])


#werte in tabelle schreiben
write('build/tabelle_alle_wellenlangen.tex', make_table([spannung, rot, grun, lila, blau, uv],[2,0,0,0,0,0]))
write('build/tabelle_orange_wellenlange.tex', make_table([spannung_orange, orange],[2,0]))



#pikoampere in ampere umrechnen
matrix = matrix*10**-12
orange = orange*10**-12




#Werte mit positivem strom heraussuchen und plotten
matrix_plus=matrix
for j in range(0,5):
	for i in range (0,len(matrix[j,:]-1)):
		if (matrix[j,i] < 0):
			matrix_plus[j,i] = np.nan
			

#wellenlangen plotten
plt.plot(spannung, 10**6*np.sqrt(matrix_plus[0,:]), 'ro', label='rot')
plt.plot(spannung, 10**6*np.sqrt(matrix_plus[1,:]), 'go', label='grün')
plt.plot(spannung, 10**6*np.sqrt(matrix_plus[2,:]), 'mo', label='lila')
plt.plot(spannung, 10**6*np.sqrt(matrix_plus[3,:]), 'bo', label='blau')
plt.plot(spannung, 10**6*np.sqrt(matrix_plus[4,:]), 'ko', label='UV')

plt.xlim(-2,2)
plt.ylabel(r'Wurzel des Stromes $10^{-6}$ / $\sqrt{\mathrm{I}}$')
plt.xlabel(r'Spannung / V')
plt.legend(loc='best')
plt.savefig('build/AlleWellenlangen.png')
plt.show()


def  g(spannung, m, b):
    		return m*(spannung) + b


U_gegen = np.zeros(5) #die gegenspannugn wird für den zweiten aufgabenteil verwendet
print(U_gegen)
# die regression für alle Spektrallinien
for i in range (0,5):
	mask = np.isfinite(matrix[i])
	parameters, popt = curve_fit(g, spannung[mask], np.sqrt(matrix[i, mask]))
	m = ufloat(parameters[0], np.sqrt(popt[0,0]))
	b = ufloat(parameters[1], np.sqrt(popt[1,1])) 
	Ug = - (b/m)
	U_gegen[i] = Ug.n
	#plots erstellen
	x = np.linspace(-2, 2)
	null = np.zeros(50) #da linspace 50 werte erzeugt
	plt.plot(x, 10**6*g(x, *parameters), 'k-')
	plt.plot(spannung, 10**6*np.sqrt(matrix_plus[i,:]), 'rx')
	plt.plot(x, null, 'k-')
	plt.xlim(-2,2)
	plt.ylabel(r'Wurzel des Stromes $10^{-6}$ / $\sqrt{\mathrm{I}}$')
	plt.xlabel(r'Spannung / V')
	plt.savefig('build/regression_Farbe:'+str(i)+'.png')
	plt.show()
	#daten speichern
	write('build/Steigung_'+str(i)+'.tex', make_SI(m*10**6, r'\sqrt{\ampere}\per\volt', 'e-6', figures=1))
	write('build/y-Achsenabschnitt_'+str(i)+'.tex', make_SI(b*10**6, r'\sqrt{\ampere}', 'e-6', figures=1))
	write('build/Grenzspannung_'+str(i)+'.tex', make_SI(Ug, r'\volt', figures=1))
		


#aufgabe 2:

#wellenlangen in nanometer (von wikipedia - muss noch genau nachgeschaut werden!!!)
L_rot = 615
L_grun = 546
L_lila = 435
L_blau = 405
L_uv = 365
L = np.array([L_rot, L_grun, L_lila, L_blau, L_uv])
#Wellenlängen übergeben:
for i in range(0,5):
	write('build/Wellenlange_'+str(i)+'.tex', make_SI(L[i], r'\nano\meter', figures=0))





# in frequenz (1/s) umrechnen:
c = 298792458 #Lichtgeschwindgkeit in m/s
n= c/(L*10**-9)

def  f(n, m, b):
    		return m*(n) + b
    		
parameters, popt = curve_fit(f, n, U_gegen)

x = np.linspace(4.5e14, 8.5e14)
plt.plot(x, f(x, *parameters), 'k-')
plt.plot(n, U_gegen, 'rx')
#plt.xlim(-2,2)
plt.ylabel(r'Grenzspannung / V')
plt.xlabel(r'Frequenz / $\nu$')
plt.savefig('build/regression_aufgabe2.png')
plt.show()

#Placksches wisckungsquantum durch elementarladung
write('build/h_durch_e.tex', make_SI(ufloat(parameters[0],np.sqrt(popt[0,0]))*10**15, r'\volt\second','e-15', figures=2))

write('build/h_durch_e_2.tex', make_SI(ufloat(parameters[0],np.sqrt(popt[0,0]))*10**15, r'\electronvolt\second','e-15', figures=2))

write('build/austrittsarbeit.tex', make_SI(ufloat(parameters[1],np.sqrt(popt[1,1])), r'\volt', figures=2))

write('build/austrittsarbeit_2.tex', make_SI(-ufloat(parameters[1],np.sqrt(popt[1,1])), r'\electronvolt', figures=2))


write('build/tabelle_h_druch_e.tex', make_table([U_gegen, L, n*10**-12],[2,0,0]))




# Aufgabe 3, plotten der orangenen skektrallinie

x=np.linspace(-20,20)
plt.plot(spannung_orange, 10**12*orange, 'bx')
plt.xlim(-20,20)
plt.ylabel(r'Photoenstrom / pA')
plt.plot(x, np.zeros(50), 'k-')
plt.xlabel(r'Spannung / V')
plt.savefig('build/OrangeWellenlange.png')
plt.show()



    	



