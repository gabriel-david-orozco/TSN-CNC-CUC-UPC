#/bin/bash

#Esta es la cantidad de variables necesaria

cp /Users/gabriel/Downloads/plantilla_Auto.docx  /Users/gabriel/Downloads/nuevo_officio.docx
for variable in FECHA_OFFICIO NUMERO_OFFICIO NOMBRE_ACCIONANTE CORREO_ACCIONANTE CELULAR_ACCIONANTE CIUDAD_ACCIONANTE NOMBRE_ACCIONADO NUM_RADICADO NUM_AUTO
do
  echo Ingrese la variable $variable
  read -r variable_value
  sed -i "s/$variable/$variable_value/g" "/Users/gabriel/Downloads/nuevo_officio.docx"
done
