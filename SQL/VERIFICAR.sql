SELECT 
TG_ENLACE, COUNT("NUMBER") CONTAR,
TG_COUNTRY_CODE
FROM PROBSUMMARYM2
INNER JOIN DEVICE2M1 ON DEVICE2M1.LOGICAL_NAME=PROBSUMMARYM2.TG_ENLACE

GROUP BY TG_ENLACE
ORDER BY CONTAR DESC;


SELECT 
M2.TG_ENLACE,
DEVICE2M1.TG_COUNTRY_CODE, 
COUNT(M1."NUMBER") CONTAR

FROM PROBSUMMARYM1 M1

INNER JOIN PROBSUMMARYM2 M2 ON M1."NUMBER"=M2."NUMBER"

INNER JOIN DEVICE2M1 ON DEVICE2M1.LOGICAL_NAME=M2.TG_ENLACE

WHERE M1.CLOSE_TIME BETWEEN '20220701'  AND '20220801'

GROUP BY TG_ENLACE



-----
INTELCOM_DEFAULT_GT
DEFAULT_COSTA RICA
DEFAULT_EL_SALVADOR
DEFAULT_HONDURAS
DEFAULT_NICARAGUA
ENLACE DEFAULT
ENLACE_DEFAULT_SV
ESC_HN_DEF001
MASIVO_CR0
MASIVO_GT
MASIVO_HN
MASIVO_NI
MASIVO_REGIONAL
MASIVO_SV
0
0

XT - ACCESO EMPRESARIAL
XT - ACTIVOS
XT - DATA_CENTER
XT - DATOS
XT - INTERNET
XT - MASIVO

TOMAR EN CUENTA MAYOR > 1
>1


TG_CRONTRY  = NULL