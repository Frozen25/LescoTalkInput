

vecmin , vecmax = [999,999,999] , [0,0,0]

print('obtener el menor de 3 colores hsv')
for i in range(3):
	print('Hue: ')
	x=int(input())
	print ('Saturation')
	y=int(input())
	print('Value')
	z=int(input())

	pixelvec = [x,y,z]

	if (pixelvec[0] > vecmax[0]):
		vecmax[0] = pixelvec[0] 
	if (pixelvec[1] > vecmax[1]):
		vecmax[1] = pixelvec[1] 
	if (pixelvec[2] > vecmax[2]):
		vecmax[2] = pixelvec[2] 
	if (pixelvec[0] < vecmin[0]):
		vecmin[0] = pixelvec[0] 
	if (pixelvec[1] < vecmin[1]):
		vecmin[1] = pixelvec[1] 
	if (pixelvec[2] < vecmin[2]):
		vecmin[2] = pixelvec[2] 


print (vecmax)
print (vecmin)