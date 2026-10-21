INSTITUTO NACIONAL DE ESTADISTICA

E INFORMATICA

## ENCUESTA NACIONAL DE HOGARES

## 2025

## VARIABLES CALCULADAS METODOLOGÍA PARA LA OBTENCIÓN DE (SUMARIA)

Lima, abril de 2026


## ESPECIFICACIONES PARA LA OBTENCIÓN DE LA SUMARIA - ENAHO 2025

## OBJETIVO

La sumaria de la ENAHO (Encuesta Nacional de Hogares) es una base de datos que resume la información más relevante de la encuesta. Sirve principalmente para análisis rápidos y comparaciones generales, ya que contiene variables ya procesadas y consolidadas a nivel de hogar.

## FACTOR DE EXPANCION, MIEMBROS, TOTAL PERSONAS, PERCEPTOR

- 1. FACTOR07 = Factor de Expansión de Población (Antes FACTORHO)

(P204 =1 (P204 = 2 P206 = 1))

- 2. Total de miembros del hogar (1)

P204=1 (P203 8, 9)

MIEPERHO =

- 3. Total, de personas en el hogar (1)

(P204=1 (P204=2 P206 = 1))

TOTMIEHO =

- 4. Total de perceptores de ingresos (1)

P204=1 (P203¹8,9) P208A 14 (I524-A>0 D529>0 I530A>0 I536>0 I538-A>0 D540>0 I541A>0 I543>0 D544T>0 D556T1>0 D556T2>0 D557T>0 D558T>0)

PERCEPHO = P500N

- 1.1 AGREGACION DE LOS GASTOS DEL HOGAR

- a. OBJETIVO

Agregar la información de gastos a nivel de hogar, anualizando y llevando los valores monetarios a un mismo período de investigación, los datos han sido agrupados

convenientemente para facilitar su procesamiento y análisis.

- b. DEFINICION OPERATIVA DEL GASTO

- La metodología del gasto se desarrollará teniendo en cuenta su estandarización con el SCN. Se desagrega los gastos por la forma de adquisición como compra, autoconsumo, auto suministro, pago en especie, donado público y privado y a nivel de 8 grupos de consumo.

Por ejemplo, con respecto a los gastos de alimentos consumidos dentro del hogar esta resumido en variables independientes aquellos alimentos que el hogar compro, recibió como pago en especie, donado público, donado privado, recibió de programas sociales, de autoconsumo/autosuministro, otra forma.

- 1. Gasto por alquiler

P105A = 1 P105B > 0 GA03HD = I105B

P201

P201


- 2. Gasto por alquiler imputado

P105A = 2,3,4,5,6,7 P106 > 0

GA04HD = I106

- 3. Gastos por alimentos consumidos fuera del hogar – Otros - Pagó

P204=1 (P203¹8,9) P208A 14 P559-D(i) > 0 T559-B(i) = 1:6, 8, 10, 15:20 P559-C(i) = 1;

G05HD = I559-D(1) + I559-D(2) + ….+ I559-D(n)

- 4. Gastos por alimentos consumidos fuera del hogar – Otro Hogar - Pagó

P204=1 (P203¹8,9) P208A 14 P559-D(i) > 0 T559-B(i) = 7 P559-C(i) = 1;

G05HD1 = I559-D(1) + I559-D(2) + ….+ I559-D(n)

- 5. Gastos por alimentos consumidos fuera del hogar – Prepara sus alimentos - Pagó

P204=1 (P203¹8,9) P208A 14 P559-D(i) > 0 T559-B(i) = 9 P559-C(i)

= 1;

G05HD2 = I559-D(1) + I559-D(2) + ….+ I559-D(n)

- 6. Gastos por alimentos consumidos fuera del hogar – Prepara sus alimentos en el Centro de Trabajo - Pagó

P204=1 (P203¹8,9) P208A 14 P559-D(i) > 0 T559-B(i) = 11 P559- C(i) = 1;

G05HD3 = I559-D(1) + I559-D(2) + ….+ I559-D(n)

- 7. Gastos por alimentos consumidos fuera del hogar – Aula del Instituto - Pagó

P204=1 (P203¹8,9) P208A 14 P559-D(i) > 0 T559-B(i) = 12 P559- C(i) = 1;

G05HD4 = I559-D(1) + I559-D(2) + ….+ I559-D(n)

- 8. Gastos por alimentos consumidos fuera del hogar – Autosuministro - Pagó

P204=1 (P203¹8,9) P208A 14 P559-D(i) > 0 T559-B(i) = 13 P559- C(i) = 1;

G05HD5 = I559-D(1) + I559-D(2) + ….+ I559-D(n)

- 9. Gastos por alimentos consumidos fuera del hogar – Campamento - Pagó

P204=1 (P203¹8,9) P208A 14 P559-D(i) > 0 T559-B(i) = 14 P559- C(i) = 1;

G05HD6 = I559-D(1) + I559-D(2) + ….+ I559-D(n)

- 10. Gastos por alimentos consumidos fuera del hogar – Alimentos Crudos Preparados - Pagó


P204=1 (P203¹8,9) P208A 14 P559-D(i) > 0 T559-B(i) = 21 P559- C(i) = 1;

G05HD7 = I559-D(1) + I559-D(2) + ….+ I559-D(n)

- 11. Gastos por alimentos consumidos fuera del hogar – Otros – NO Pagó

P204=1 (P203¹8,9) P208A 14 P559-D(i) > 0 T559-B(i) = 1:6, 8, 10, 15:20 P559-C(i) = 2;

IG06HD = I559-D(1) + I559-D(2) + ….+ I559-D(n)

- 12. Gastos por alimentos consumidos fuera del hogar – Otro Hogar – NO Pagó

P204=1 (P203¹8,9) P208A 14 P559-D(i) > 0 T559-B(i) = 7 P559-C(i) = 2;

IG06HD1 = I559-D(1) + I559-D(2) + ….+ I559-D(n)

- 13. Gastos por alimentos consumidos fuera del hogar – Prepara sus Alimentos – NO Pagó

P204=1 (P203¹8,9) P208A 14 P559-D(i) > 0 T559-B(i) = 9 P559-C(i) = 2;

IG06HD2 = I559-D(1) + I559-D(2) + ….+ I559-D(n)

- 14. Gastos por alimentos consumidos fuera del hogar – Prepara sus alimentos en su Centro de Trabajo – NO Pagó

P204=1 (P203¹8,9) P208A 14 P559-D(i) > 0 T559-B(i) = 11 P559- C(i) = 2;

IG06HD3 = I559-D(1) + I559-D(2) + ….+ I559-D(n)

- 15. Gastos por alimentos consumidos fuera del hogar – Aula del Instituto – NO Pagó

- P204=1 (P203¹8,9) P208A 14 P559-D(i) > 0 T559-B(i) = 12 P559- C(i) = 2;

IG06HD4 = I559-D(1) + I559-D(2) + ….+ I559-D(n)

- 16. Gastos por alimentos consumidos fuera del hogar – Autosuministro – NO Pagó

P204=1 (P203¹8,9) P208A 14 P559-D(i) > 0 T559-B(i) = 13 P559- C(i) = 2;

IG06HD5 = I559-D(1) + I559-D(2) + ….+ I559-D(n)

- 17. Gastos por alimentos consumidos fuera del hogar – Campamento – NO Pagó

- 2; P204=1 (P203¹8,9) P208A 14 P559-D(i) > 0 T559-B(i) = 14 P559- C(i) =

IG06HD6 = I559-D(1) + I559-D(2) + ….+ I559-D(n)

- 18. Otros Gastos transporte - Pagó


G07HD =

I560-D(1) + I560-D(2) + I560-D(3) + I560-D(4) + I560-D(5) + I560-

D(6)

- 19. Ingresos y Gastos, Otros - No Pagó

- 20. Grupo 1: Alimentos - Gasto

- 21. Grupo 1: Alimentos - Autosuministro, Autoconsumo

- 22. Grupo 1: Alimentos - Pago en especie

- 23. Grupo 1: Alimentos – Donación Público

- 24. Grupo 1: Alimentos – Donación Privada

- 25. Grupo 1: Alimentos – otros

- 26. Grupo 1: Alimentos - Donado, regalado, otro (Bienes Libres 2)

- 27. Grupo 1: Alimentos preparados consumir en el hogar - Pagado


I601-C(i) > 0 (P601-A1(i) = 1); ( i ) = 47, 50

GRU14HD = I601-C(i)

- 28. Grupo 1: Alimentos preparados consumir en el hogar - Autoconsumo , auto suministro

I601-E(i) > 0 (P601-A2(i) = 1 P601-A3(i) = 1); ( i ) 47, 50

GRU14HD1 = I601-E(i)

- 29. Grupo 1: Alimentos preparados consumir en el hogar - Especie

I601-E(i) > 0 (P601-A4(i) = 1); ( i ) 47, 50

GRU14HD2 = I601-E(i)

- 30. Grupo 1: Alimentos preparados consumir en el hogar - Donado publico

I601-E(i) > 0 (P601-A6(i) = 1); ( i ) 47, 50

GRU14HD3 = I601-E(i)

- 31. Grupo 1: Alimentos preparados consumir en el hogar - Donado privado

I601-E(i) > 0 (P601-A5(i) = 1); ( i ) 47, 50

GRU14HD4 = I601-E(i)

- 32. Grupo 1: Alimentos preparados consumir en el hogar - otro

I601-E(i) > 0 (T601-A71(i) = 1); ( i ) 47, 50

GRU14HD5 = I601-E(i)

- 33. Grupo 1: Alimentos consumidos Fuera del Hogar -Bienes libres

I601-E(i) > 0 T601-A72(i) = 1 ; ( i ) 47, 50

GRU14HD6 = I601-E(i)

- 34. Gastos por alimentos para consumir dentro del hogar obtenidos de instituciones benéficas- pagado

P602-D1(i) = 1 I602-E1(i) > 0

P602-D1(i) = 2 I602-E2(i) > 0

SG23 = (I602-E1(1) + . + I602-E1(7) + I602-E2 (1) + …+ I602-E2 (7)

- 35. Ingresos y Gastos por alimentos para consumir dentro del hogar (no pago)

P602-D1(i) = 3 I602-E2(i) > 0

SIG24 = (I602-E1(1) + I602-E1(2) + …. + I602-E1(7))

- 36. Gastos por alimentos consumidos fuera del hogar de instituciones benéficas- pagado

P602-D2(i) = 1 I602-E3(i) > 0


- 37. Ingresos y Gastos por alimentos consumidos fuera del hogar de instituciones benéficas- pagado (no pago)

- 38. Gastos por alimentos preparados obtenidos de la olla común - pagado

- 39. Ingresos y Gastos por alimentos preparados de la olla común- no pago

- 40. Grupo 2: Vestido y Calzado - Gasto

- 41. Grupo 2: Vestido y Calzado – Autoconsumo, Autosuministro

- 42 Grupo 2: Vestido y Calzado - Pago en especie

- 43. Grupo 2: Vestido y Calzado – Donación Pública

- 44. Grupo 2: Vestido y Calzado – Donación Privada


- 45. Grupo 2: Vestido y Calzado – Otro

- 46. Grupo 2: Vestido y Calzado - No gasto, no sabe

- 47. Grupo 3: Alquiler de Vivienda, Combustible, Electricidad y Conservación de la Vivienda - Gasto

- 48. Grupo 3: Alquiler de Vivienda, Combustible, Electricidad y Conservación de la Vivienda – Autoconsumo, Autosuministro

- 49. Grupo 3: Alquiler de Vivienda, Combustible, Electricidad y Conservación de la Vivienda - Pago en especie

- 50. Grupo 3: Alquiler de Vivienda, Combustible, Electricidad y Conservación de la Vivienda – Donación Pública

- 51. Grupo 3: Alquiler de Vivienda, Combustible, Electricidad y Conservación de la Vivienda – Donación Privada

- 52. Grupo 3: Alquiler de Vivienda, Combustible, Electricidad y Conservación de la


## Vivienda - Otro

(P603-A7(14) = 1 I603-C7(14) > 0)) (P605-A5(5,6) = 1 I605-C5(5,6) > 0)) (P611-A6(5) = 1 I611-C6(5) > 0))

GRU33HD3 = I603-C2(14) + I603-C7(14)+ I605-C5(5,6)+ I611-C6(5)

- 53. Grupo 3: Alquiler de Vivienda, Combustible, Electricidad y Conservación de la Vivienda – imputado, No gastó, no sabe

- 54. Grupo 4: Muebles y Enseres, y Mantenimiento de la Vivienda - Gasto

- 55. Grupo 4: Muebles y Enseres, y Mantenimiento de la Vivienda – Autoconsumo - Autosuministro

- ((P603-A2(1:13,15)=1ÚP603-A3(1:13,15)=1)Ù(I603-C2(1:13,15)ÚI603-C3(1:13, 15)> 0 )) ((P610-A2(1,3:6) = 1P610-A3(1,3:6) = 1)(I610-C2(1,3:6) I610- C3(1,3:6))> 0 )

- 56. Grupo 4: Muebles y Enseres, y Mantenimiento de la Vivienda - Pago en especie

- 57. Grupo 4: Muebles y Enseres, y Mantenimiento de la Vivienda – Donación Pública

- ((P603-A6(1:13,15)=1)Ù(I603-C6(1:13,15)> 0)Ú ((P610-A6(1,3:6) = 1)Ù(I610- C6(1,3:6)> 0 )

- 58. Grupo 4: Muebles y Enseres, y Mantenimiento de la Vivienda – Donación Privada

GRU42HD1=I603-C2(1:13,15)+I603-C5(1:13,15)+ I605-C2(2:4,7,8)+I610- C5(1,3:6)


- 59. Grupo 4: Muebles y Enseres, y Mantenimiento de la Vivienda - Otros

- GRU42HD1= I603-C2(1:13, 15) + I603-C7(1:13, 15) + I605-C5(2:4,7,8)+ I610- C7(1,3:6)

- 60. Grupo 4: Muebles y Enseres, y Mantenimiento de la Vivienda - No gastó, no sabe

GRU44HD = I603-B(1:13, 15) + I605-B(2:4,7,8) + I605-C3(2:4,7,8)+ I610-B(1,3:6)

- 61. Grupo 5: Cuidado, Conservación de la Salud y Servicios Médicos - Gasto

- 62. Grupo 5: Cuidado, Conservación de la Salud y Servicios Médicos – Autosuministro, Autoconsumo

GRU52HD1 = I4182(i)+ (I4183(i)

- 63. Grupo 5: Cuidado, Conservación de la Salud y Servicios Médicos – Donación Pública

- 64. Grupo 5: Cuidado, Conservación de la Salud y Servicios Médicos – Donación Privada

- 65. Grupo 5: Cuidado, Conservación de la Salud y Servicios Médicos - Otros

- 66. Grupo 5: Cuidado, Conservación de la Salud y Servicios Médicos – Otros Bienes libres

- 67. Grupo 5: Cuidado, Conservación de la Salud y Servicios Médicos - No gastó, no sabe


- 68. Grupo 6: Transportes y Comunicaciones – Gasto

- 69. Grupo 6: Transportes y Comunicaciones - Autosuministro, Autoconsumo

- 70. Grupo 6: Transportes y Comunicaciones - Pago en especie

- 71. Grupo 6: Transportes y Comunicaciones – Donación Pública

- 72. Grupo 6: Transportes y Comunicaciones – Donación Privada

- 73. Grupo 6: Transportes y Comunicaciones – Otro

- 74. Grupo 6: Transportes y Comunicaciones - No gastó, no sabe

- 75. Grupo 7: Esparcimiento, Diversión, Servicios Culturales y de Enseñanza - Gasto


- 76. Grupo 7: Esparcimiento, Diversión, Servicios Culturales y de Enseñanza - Autosuministro, Autoconsumo

- 77. Grupo 7: Esparcimiento, Diversión, Servicios Culturales y de Enseñanza - Pago en especie

- 78. Grupo 7: Esparcimiento, Diversión, Servicios Culturales y de Enseñanza – Donación Pública

- 79. Grupo 7: Esparcimiento, Diversión, Servicios Culturales y de Enseñanza – Donación Privada

- 80. Grupo 7: Esparcimiento, Diversión, Servicios Culturales y de Enseñanza - Otros

- 81. Grupo 7: Esparcimiento, Diversión, Servicios Culturales y de Enseñanza - No gastó, no sabe


- 82. Grupo 8: Otros Bienes y Servicios - Gasto

- 83. Grupo 8: Otros Bienes y Servicios - Autosuministro, Autoconsumo

- 84. Grupo 8: Otros Bienes y Servicios - Pago en especie

- 85. Grupo 8: Otros Bienes y Servicios – Donación Pública

- 86. Grupo 8: Otros Bienes y Servicios – Donación Privada

- 87. Grupo 8: Otros Bienes y Servicios - Otros

- 88. Grupo 8: Alimentos para mascotas - bien libre

- 89. Grupo 8: Otros Bienes y Servicios - No gastó, no sabe

- 90. Grupo 8: Otros Bienes y Servicios - Otros bienes y servicios fiestas familiares y sociales - pagado


GRU84HD1 = I611-B(12)

- 91. Grupo 8: Otros bienes y servicios fiestas familiares y sociales- autoconsumo, auto suministro

T611N =12 (P611-A2(9)=1 P611-A3(9)=1 (I611-C2(9) I611-C3(9))> 0) GRU85HD1 = I611-C2(9)+ I611-C3(9)

- 92. Grupo 8: Otros bienes y servicios fiestas familiares y sociales- donado privado

T611N =12 (P611-A4(9)=1 P611-A3(9)=1 (I611-C3(9) I611-C4(9))> 0)

- 93. Grupo 8: Otros bienes y servicios fiestas familiares y sociales- donado - otro

T611N =12 (P611-A6(9)=1 P611-A3(9)=1 (I611-C6(9) I611-C3(9))> 0)

GRU86HD2 = 611-C3(9)+ I611-C6(9)

- 94. Grupo 8: Otros bienes y servicios fiestas familiares y sociales- no gastó, no sabe

GRU87HD = 611-C5(9)

- 95. Gastos por Equipamiento del hogar compra – TV, computadora, sonido

(P612-A (1:7) = 1 P612 = 1 P612B = 1

- 96. Gastos por Equipamiento del hogar compra – Electrodomésticos

(P612-A (8:15) = 1 P612 = 1 P612B = 1

- 97. Gastos por Equipamiento del hogar compra – Transporte

(P612-A (16:21) = 1 P612 = 1 P612B = 1;

- 98. Gastos por Equipamiento del hogar compra – Otros

- 99. Gastos por Equipamiento del hogar donado – TV., computadora, sonido

- 100. Gastos por Equipamiento del hogar donado – Electrodomésticos


(P612-A (8:15) = 1 P612 = 1 P612B = 1

- 101. Gastos por Equipamiento del hogar DONADOS – Transporte

(P612-A (16:21) = 1 P612 = 1 P612B = 1

- 102. Gastos por Equipamiento del hogar donado – Otros

(P612-A (22:26) = 1 P612 = 1 P612B = 1

SG42D3 = I612-G

## 1.1 ANUALIZACION DEL INGRESO MONETARIO

## a. OBJETIVO

Agregar la información de Ingresos a nivel de hogar, anualizando y llevando los valores monetarios a un mismo período de investigación, para su posterior procesamiento y análisis.

## b. DEFINICION OPERATIVA DEL INGRESO MONETARIO

Los Ingresos del hogar son las retribuciones monetarias y/o en especie, que reciben los miembros del hogar durante el período de referencia. Se incluye también el consumo por autoconsumo, autosuministro, donados público y donado privado a nivel de 12 grupos de consumo.

(1) Se consideran a todas las personas que en la P201 que hayan o no omitido el Capítulo Empleo e Ingreso.

(2) Para el cálculo de los ingresos no se consideran aquellas personas que han omitido el Capítulo Empleo e Ingreso. Preguntas: (P501- P5040) = Missing (P505 - P544) = b

## 1. Ingresos obtenido por crédito a algún miembro del hogar - comprar casa departamento.

P107B1= 1 D107D1 >0

IG03HD1 = D107D1

- 2. Ingresos obtenido por crédito a a l gún miembro del hogar - comprar terreno para vivienda.

P107B2= 1 D107D2 >0

IG03HD2 = D107D2

- 3. Ingresos obtenido por crédito a algún miembro del hogar - Mejoramiento y/o ampliación de la vivienda.

P107B3= 1 D107D3 >0

IG03HD3 = D107D3

- 4. Ingresos obtenido por crédito a a l gún miembro del hogar - Construcción de vivienda nueva.


P107B4= 1 D107D4>0

IG03HD4 = D107D4

- 5. Ingreso bruto de la actividad principal monetario (dependiente) (2)

P204=1

(P203¹8,9) P208A 14 P507=3,4,6,7

I524-A > 0

v

A

A

NGBRUHD = I524-A

- 6. Ingreso neto de la actividad principal monetario (dependiente) (2)

P204=1 (P203¹8,9)

P208A P507=3,4,6,7

I524-E > 0

I524-B 0

A

A

A

z

INGNETHD =

I524- E

- 7. Ingreso por pago en especie de la actividad principal, (2)

P204=1

(P203¹8,9) P208A 14 P507=3,4,6,7

A

PAGESPHD = (D529T)

- 8. Ingreso por actividad principal independiente (2)

P204=1

(P203¹8,9)

P208A 14

P507=1,2

A

A

A

z

INGINDHD =

I530A

- 9. Ingreso por autoconsumo de la actividad principal independiente, (2)

P204=1

(P203¹8,9)

P208A 14

P507=1,2

A

A

A

INGAUTHD = D536

- 10. Ingreso bruto de la actividad secundaria dependiente(2)

A P208A A P507=1:4,6,7 A [[P514=1 v (P514=2 A

P204=1 A

P515=1(Al menos una alternativa))])]

INSEDTHD = I538-A

- 11. Ingreso neto de la actividad secundaria dependiente(2)

A P208A A P507=1:4,6,7 A [[P514=1 v (P514=2 A

P204=1 A

P515=1(Al menos una alternativa))])]

INSEDLHD = I538-E

- 12. Ingreso pago en especie de la actividad secundaria dependiente(2)

A P208A A P507=1:4,6,7 A [[P514=1 v (P514=2 A

P204=1 A

P515=1(Al menos una alternativa))])]

PAESECHD = (D540T)


## 13. Ingreso neto de la actividad secundaria independiente(2)

A P208A A P507=1:4,6,7 A [[P514=1 v (P514=2 A

P204=1 A

P515=1(Al menos una alternativa))])]

INGSEIHD = I541A

- 14. Ingreso por autoconsumo de la actividad secundaria independiente(2)

P208A P507=1:4,6,7 [[P514=1 v (P514=2

P204=1

P515=1(Al menos una alternativa))])]

z

ISECAUHD =

- 15. Ingresos extraordinarios por trabajo(2)

P204=1

A

INGEXTHD = D544T

- 16. Ingreso por transferencias corrientes monetarias del país(2)

P204=1

A

INGTRAHD = D556T1

- 17. Ingreso por transferencias corrientes del extranjero (2)

P204=1

A

INGTEXHD = D556T2

- 18. Ingreso por Transferencia corrientes Privada

P204=1 D556T3 =

A z

D556ic + D556ie (i)

INGTPRHD = D556T3

- 19. Ingreso por Transferencia corrientes Juntos

P204=1

A

D556T4 = D556ic

INGTPU01 = D556T4

- 20. Ingreso por Transferencia corrientes Pensión 65

P204=1

A

D556T5 = D556ic

z

INGTPU03 =

- 21. Ingreso por Transferencia corrientes Beca 18

P204=1 (P203¹8,9) P208A 14 P556-iA (i = 10) D556T6 = D556ic

INGTPU04 = D556T10

D543

(P203¹8,9) P208A 14 (P507=3,4,6,7 P517=3,4,6,7)

(P203¹8,9)

P208A 14

A

(P203¹8,9)

P208A 14

A

(P203¹8,9)

P208A 14 P556-iA (i =1,2,3,9)

A

(P203¹8,9)

P208A 14 P556-iA (i = 6)

A

(P203¹8,9)

P208A 14 P556-iA (i = 7)

A

D556T5


## 22. Ingreso por Transferencia corrientes Bono de Gas

P204=1 (P203¹8,9) P208A 14 T556-iA (i =11) D556T11 = D556ic

INGTPU05 = D556T11

- 23. Ingreso por Transferencia corrientes Bono electricidad

P204=1 (P203¹8,9) P208A 14 T556-iA (i =20) D556T20 = D556ic

INGTPU10 = D556T20

- 24. Ingreso por Transferencia corrientes Bono Niño

P204=1 (P203¹8,9) P208A 14 T556-iA (i =21) D556T21 = D556ic

INGTPU11 = D556T21

- 25. Ingreso por Transferencia corrientes Bono ONP

P204=1 (P203¹8,9) P208A 14 T556-iA (i =22) D556T22 = D556ic

INGTPU12 = D556T22

- 26. Ingreso por Transferencia corrientes Bono contigo

P204=1 (P203¹8,9) P208A 14 T556-iA (i =23) D556T23 = D556ic

INGTPU13 = D556T23

## 30. Ingreso por Transferencia corrientes Públicas TOTAL

P204=1 (P203¹8,9) P208A 14 P556-iA (i =4,5,6,7,8,10,11, 20,21,22,23)) INGTPUHD = D556ic + D556ie

- 31. Ingreso por Otras Transferencia corrientes Pública (sin Juntos, sin Pensión

65, sin Beca 18, sin Bono Gas, sin Bono Electricidad, sin Bono Niño, sin Bono ONP, sin Bono Contigo)

INGTPU02 = INGTPUHD - INGTPUi (i =1,3,4,5,10,11,12,13)

- 32. Ingreso por rentas de la propiedad monetario(2)

P204=1 (P203¹8,9) P208A 14

INGRENHD = D557T

- 33. Otros Ingresos Extraordinarios (2)

P204=1 (P203¹8,9) P208A 14

INGOEXHD = D558T

- 34. Ingreso alquiler imputado de la vivienda


P105A = 2,3,4,6,7 P106 > 0

## IA01HD = I106

## 35. Ingreso por transferencia de alquiler

P105A = 5 P106 > 0

IA02HD = I106

## Ingresos Monetario (1)

- 01. INGMO1HD(BRUTO)= INGBRUHD +INGINDHD +INSEDTHD +INSEDTHD +INGSEIHD1 INGEXTHD +INGTRAHD +INGTEXHD +INGRENHD+ INGOEXHD

02. INGMO2HD(NETO) = INGNETHD +INGINDHD+ INSEDLHD+ INGSEIHD+ INGEXTHD +INGTRAHD +INGTEXHD +INGRENHD +INGOEXHD

## Ingresos total anuales (2)

## 03. INGHOG1D(BRUTO) = (INGBRUHD + INGINDHD + INSEDTHD +

INGSEIHD + INGEXTHD + INGTRAHD + INGTEXHD + INGRENHD + INGOEXHD + PAGESPHD + INGAUTHD + PAESECHD + ISECAUHD + IA01HD -GA04HD + IG06HD + IG08HD + SIG24 + SIG26 + SIG28 + GRU13HD1 + GRU13HD2 + GRU13HD3 + GRU23HD1 + GRU23HD2 + GRU23HD3 + GRU24HD + GRU33HD1 + GRU33HD2 + GRU33HD3 + GRU34HD + GRU43HD1 + GRU43HD2 + GRU43HD3 + GRU44HD + GRU53HD1 + GRU53HD2 + GRU53HD3 + GRU54HD + GRU63HD1 + GRU63HD2 + GRU63HD3 + GRU64HD + GRU73HD1 + GRU73HD2 + GRU73HD3 + GRU74HD + GRU83HD1 + GRU83HD2 + GRU83HD3 + GRU84HD + GRU14HD3 + GRU14HD4 + GRU14HD5 + SG42D + SG42D1 + SG42D2 + SG42D3)

*Nota se resta el ingreso imputado ga04hd por estar incluido dentro del grupo de autoconsumo GRU34HD.

## 04. INGHOG2D(NETO) = ( INGNETHD + INGINDHD + INSEDTHD +

INGSEIHD + INGEXTHD + INGTRAHD + INGTEXHD + INGRENHD + INGOEXHD + PAGESPHD + INGAUTHD + PAESECHD + ISECAUHD + IA01HD + -GA04HD + IG06HD + IG08HD + SIG24 + SIG26 +SIG28 + GRU13HD1 + GRU13HD2 + GRU13HD3 + GRU23HD1 + GRU23HD2 + GRU23HD3 + GRU24HD + GRU33HD1 + GRU33HD2 + GRU33HD3 + GRU34HD + GRU43HD1 + GRU43HD2 + GRU43HD3 + GRU44HD + GRU53HD1 + GRU53HD2 + GRU53HD3 + GRU54HD + GRU63HD1 + GRU63HD2 + GRU63HD3 + GRU64HD + GRU73HD1 + GRU73HD2 + GRU73HD3 + GRU74HD + GRU83HD1 + GRU83HD2 + GRU83HD3 + GRU84HD + GRU14HD3 + GRU14HD4 + GRU14HD5 + SG42D + SG42D1 + SG42D2 + SG42D3)

## 05. Gasto Monetario Anuales (3)

```
= G05HD + G05HD1 + G05HD2 + G05HD3 + G05HD4 + G05HD5 + G05HD6 + G07HD + SG23 + SG25 +
GASHOG1D
```


SG27+ GRU21HD + GRU11HD + GRU14HD + GRU31HD + GRU41HD + GRU51HD + GRU61HD + GRU71HD + GRU81HD + SG42 + SG421 + SG422 + SG423

## 06. Gasto Total Anuales (4)

GASHOG2D = G05HD + G05HD1 + G05HD2 + G05HD3 + G05HD4 +

G05HD5 + G05HD6 + IG06HD + G07HD + IG08HD + SG23 + SIG24 + SG25 + SG27 + SIG26 + SIG28 + GRU11HD + GRU12HD1 + GRU12HD2 + GRU13HD1 + GRU13HD2 + GRU13HD3 + GRU21HD + GRU22HD1 + GRU22HD2 + GRU23HD1 + GRU23HD2 + GRU23HD3 + GRU24HD + GRU31HD + GRU32HD1 + GRU32HD2 + GRU33HD1 + GRU33HD2 + GRU33HD3 + GRU34HD + GRU41HD + GRU42HD1 + GRU42HD2 + GRU43HD1 + GRU43HD2 + GRU43HD3 + GRU44HD + GRU51HD + GRU52HD1 + GRU53HD1 + GRU53HD2 + GRU53HD3 + GRU54HD + GRU61HD + GRU62HD1 + GRU62HD2 + GRU63HD1 + GRU63HD2 + GRU63HD3 + GRU64HD + GRU71HD + GRU72HD1 + GRU72HD2 + GRU73HD1 + GRU73HD2 + GRU73HD3 + GRU74HD + GRU81HD + GRU82HD1 + GRU82HD2 + GRU83HD1 + GRU83HD2 + GRU83HD3 + GRU84HD + GRU14HD + GRU14HD1 + GRU14HD2 + GRU14HD3 + GRU14HD4 + GRU14HD5 + SG42 + SG421 + SG422 + SG423 + SG42D + SG42D1 + SG42D2 + SG42D3


## RELACION DE LAS VARIABLES – SUMARIA

Año. Mes de ejecución de la encuesta. Conglomerado. Número de selección de la vivienda. Hogar. Ubicación geográfica. Dominio. Estrato geográfico. Total, de perceptores de ingresos. Total, de miembros del hogar. Total, de personas en el hogar. Ingreso alquiler imputado de la vivienda. Ingreso por transferencia de alquiler. Crédito, compra casa, departamento. Crédito, comprar terreno para vivienda. Crédito mejoramiento y/o ampliación de la vivienda. Crédito, construcción de nueva vivienda. Gasto por alquiler. Gasto por alquiler imputado. Gastos por alimentos para consumir dentro del hogar. Ingresos y gastos por alimentos para consumir en el hogar. Gastos por alimentos consumidos fuera del hogar (menores de 14 años).

Gastos por alimentos consumidos en “Olla común”, pagado

Ingresos y gastos por alimentos consumidos fuera del hogar (menores de 14 años).

Ingreso y gasto por alimentos consumidos en “Olla común”- no pago.

Gastos por equipamiento del hogar comprados- equipos tv, computa, sonido. Gastos por equipamiento del hogar comprados- electrodomésticos. Gastos por equipamiento del hogar comprados – transporte. Gastos por equipamiento del hogar comprados- otros. Gastos por equipamiento del hogar adquiridos - equipos tv, computa, sonido. Gastos por equipamiento del hogar adquiridos- electrodomésticos. Gastos por equipamiento del hogar adquiridos- transporte. Gastos por equipamiento del hogar adquiridos- otros. Ingreso bruto actividad principal monetaria (dependiente). Ingreso neto de la actividad principal monetario (dependiente). Ingreso por pago en especie de la actividad principal. Ingreso por actividad principal independiente. Ingreso por autoconsumo de la actividad principal independiente Ingreso bruto de la actividad secundaria dependiente. Ingreso neto de la actividad secundaria dependiente. Ingreso pago en especie de la actividad secundaria dependiente. Ingreso neto de la actividad secundaria independiente. Ingreso por autoconsumo de la actividad secundaria independiente. Ingresos extraordinarios por trabajo.

aÑo mes conglome vivienda hogar ubigeo dominio estrato percepho mieperho totmieho ia01hd ia02hd ig03hd1 ig03hd2 ig03hd3 ig03hd4 ga03hd ga04hd sg23 sig24 sg25 sg27

sig26 sig28 sg42 sg421 sg422 sg423 sg42d sg42d1 sg42d2 sg42d3 ingbruhd ingnethd pagesphd ingindhd ingauthd insedthd insedlhd paesechd ingseihd isecauhd ingexthd

21


ingtrahd ingtexhd ingrenhd ingoexhd g05hd ig06hd g05hd1

Ingreso por transferencias corrientes monetarias del país. Ingreso por transferencias corrientes del extranjero. Ingreso por rentas de la propiedad monetaria. Otros ingresos extraordinarios. Gastos por alimentos consumidos fuera del hogar – pagó. Ingresos y gastos por alimentos consumidos fuera del hogar-no pago. Gastos por alimentos consumidos fuera del hogar en otro hogar- pagó. Ingresos y gastos por alimentos consumidos fuera del hogar - otro hogar-no pago. Gastos por alimentos consumidos fuera del hogar prepara sus alimentos – pagó. Ingresos y gastos por alimentos consumidos fuera del hogar - prepara sus alimentos. Gastos por alimentos consumidos fuera del hogar prepara sus alimentos en su centro de trabajo. Ingresos y gastos por alimentos consumidos fuera del hogar - prepara sus alimentos. Gastos por alimentos consumidos fuera del hogar en el aula del centro educativo. Ingresos y gastos por alimentos consumidos fuera del hogar- aula de su centro educativo. Gastos por alimentos consumidos fuera del hogar a autoconsumo. Ingresos y gastos por alimentos consumidos fuera del hogar - autoconsumo-no pago. Gastos por alimentos consumidos fuera del hogar campamento – pagó. Ingresos y gastos por alimentos consumidos fuera del hogar - campamento-no pago. Otros gastos – pagó. Ingresos y gastos, otros - no pagó. Ingreso por transferencia corrientes privada. Ingreso por transferencia corrientes pública. Ingreso por transferencia corrientes pública juntos. Ingreso por transferencias corrientes públicas otros. Ingreso por transferencias corrientes públicas pensión 65. Ingreso por transferencias corrientes públicas beca 18. Ingreso por transferencias corrientes públicas bono del gas. Ingreso por transferencias corrientes públicas: bono electricidad. Ingreso por transferencia corrientes pública: bono niño. Ingreso por transferencias corriente pública: bono onp. Ingreso por transferencias corriente pública: bono contigo. Grupo 1: alimentos – gasto. Grupo 1: alimentos - autoconsumo, auto suministro. Grupo 1: alimentos - pago en especie. Grupo 1: alimentos - donación pública. Grupo 1: alimentos - donación privada. Grupo 1: alimentos - otros gastos. Grupo 1: alimentos consumidos dentro hogar -bienes libres. Grupo 1: alimentos preparados consumir en el hogar – pagado. Grupo 1: alimentos preparados consumir en el hogar - autoconsumo ,

ig06hd1

g05hd2

ig06hd2

g05hd3

ig06hd3

g05hd4

ig06hd4 g05hd5

ig06hd5 g05hd6

ig06hd6 g07hd ig08hd ingtprhd ingtpuhd ingtpu01 ingtpu02 ingtpu03 ingtpu04 ingtpu05 ingtpu10 ingtpu11 ingtpu12 ingtpu13 gru11hd gru12hd1 gru12hd2 gru13hd1 gru13hd2 gru13hd3 gru13hd4 gru14hd

gru14hd1

autosuministro.


- gru32hd1 Grupo 1: alimentos preparados consumir en el hogar – especie. Grupo 1: alimentos preparados consumir en el hogar - donado público. Grupo 1: alimentos preparados consumir en el hogar - donado privado. Grupo 1: alimentos preparados consumir en el hogar – otros. Grupo 1: alimentos consumidos fuera del hogar -bienes libres. Grupo 2: vestido y calzado – gasto. Grupo 2: vestido y calzado - autoconsumo, autosuministro. Grupo 2: vestido y calzado - pago en especie. Grupo 2: vestido y calzado - donación pública. Grupo 2: vestido y calzado - donación privada. Grupo 2: vestido y calzado – otros. Grupo 2: vestido y calzado - no gasto, no sabe. Grupo 3: alquiler de vivienda, combustible, electricidad y conservación de la vivienda - pago. Grupo 3: alquiler de vivienda, combustible, electricidad y conservación de la vivienda-autoconsumo. Grupo 3: alquiler de vivienda, combustible, electricidad y conservación de la vivienda-especie. Grupo 3: alquiler de vivienda, combustible, electricidad y conservación de la vivienda-donado público. Grupo 3: alquiler de vivienda, combustible, electricidad y conservación de la vivienda- donado privado. Grupo 3: alquiler de vivienda, combustible, electricidad y conservación de la vivienda-otros. Grupo 3: alquiler de vivienda, combustible, electricidad y conservación de la vivienda-no sabe, no gasto. Grupo 4: muebles, enseres y mantenimiento de la vivienda - gasto Grupo 4: muebles, enseres y mantenimiento de la vivienda - autoconsumo, autosuministro. Grupo 4: muebles, enseres y mantenimiento de la vivienda - pago en especie Grupo 4: muebles, enseres y mantenimiento de la vivienda - donación pública Grupo 4: muebles, enseres y mantenimiento de la vivienda - donación privada Grupo 4: muebles, enseres y mantenimiento de la vivienda - otros Grupo 4: muebles, enseres y mantenimiento de la vivienda - no gastó, no sabe Grupo 5: cuidado, conservación de la salud y servicios médicos - gasto Grupo 5: cuidado, conservación de la salud y servicios médicos - autoconsumo,

- gru14hd2 gru14hd3 gru14hd4 gru14hd5 gru14hd6 gru21hd gru22hd1 gru22hd2 gru23hd1 gru23hd2 gru23hd3 gru24hd

- gru31hd

gru32hd2

gru33hd1

gru33hd2

gru33hd3

gru34hd gru41hd

gru42hd1 gru42hd2 gru43hd1 gru43hd2 gru43hd3 gru44hd gru51hd

gru52hd1

autosuministro. Grupo 5: cuidado, conservación de la salud y servicios médicos - donación pública Grupo 5: cuidado, conservación de la salud y servicios médicos - donación privada. Grupo 5: cuidado, conservación de la salud y servicios médicos - otros Grupo 5: cuidado, conservación de la salud y servicios médicos - bienes libres Grupo 5: cuidado, conservación de la salud y servicios médicos - no gastó, no sabe. Grupo 6: transportes y comunicaciones - gasto Grupo 6: transportes y comunicaciones - autoconsumo, autosuministro Grupo 6: transportes y comunicaciones - pago en especie Grupo 6: transportes y comunicaciones - donación pública Grupo 6: transportes y comunicaciones - donación privada

gru53hd1

gru53hd2 gru53hd3 gru53hd4

gru54hd gru61hd gru62hd1 gru62hd2 gru63hd1 gru63hd2


gru63hd3 gru64hd gru71hd

Grupo 6: transportes y comunicaciones - otros Grupo 6: transportes y comunicaciones - no gasto, no sabe Grupo 7: esparcimiento, diversión, servicios culturales y de enseñanza - gasto Grupo 7: esparcimiento, diversión, servicios culturales y de enseñanza - autoconsumo Grupo 7: esparcimiento, diversión, servicios culturales y de enseñanza - pago en especie. Grupo 7: esparcimiento, diversión, servicios culturales y de enseñanza – donación privada. Grupo 7: esparcimiento, diversión, servicios culturales y de enseñanza – donación pública. Grupo 7: esparcimiento, diversión, servicios culturales y de enseñanza - otros Grupo 7: esparcimiento, diversión, servicios culturales y de enseñanza - no gas Grupo 8: otros bienes y servicios - gasto Grupo 8: otros bienes y servicios - autoconsumo, autosuministro. Grupo 8: otros bienes y servicios - pago en especie. Grupo 8: otros bienes y servicios - donación pública. Grupo 8: otros bienes y servicios - donación privada. Grupo 8: otros bienes y servicios – otros. Grupo 8: alimentos para mascotas - bien libre. Grupo 8: otros bienes y servicios - no gastó, no sabe. Grupo 8: otros bienes y servicios fiestas familiares y sociales – pagado. Grupo 8: otros bienes y servicios fiestas familiares y sociales- autoconsumo, autosuministro. Grupo 8: otros bienes y servicios fiestas familiares y sociales- donado privado Grupo 8: otros bienes y servicios fiestas familiares y sociales- donado - otro Grupo 8: otros bienes y servicios fiestas familiares y sociales- no gastó, no sabe Ingreso monetario (bruto) Ingreso monetario (neto) Ingreso bruto Ingreso neto total Gasto monetario Gasto total bruto Factor de expansión anual. Proyecciones cpv-2007 Línea de pobreza alimentaria Línea de pobreza total Pobreza Línea corriente de vulnerabilidad Pobreza y vulnerabilidad

gru72hd1

gru72hd2

gru73hd1

gru73hd2 gru73hd3 gru74hd gru81hd gru82hd1 gru82hd2 gru83hd1 gru83hd2 gru83hd3 gru83hd4 gru84hd gru84hd1

gru85hd1 gru86hd1 gru86hd2 gru87hd ingmo1hd ingmo2hd inghog1d inghog2d gashog1d gashog2d factor07 LINPE LINEA POBREZA LINEAV POBREZAV

NCONGLOME Número de conglomerado(proveniente del marco) SUB_CONGLOME Número de Sub-conglomerado (proveniente del marco)
