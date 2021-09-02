#/bin/bash

#Esta es la cantidad de variables necesaria

cp /usr/plantilla_Auto.docx  /usr/nuevo_officio.docx
for variable in FECHA_OFFICIO NUMERO_OFFICIO NOMBRE_ACCIONANTE CORREO_ACCIONANTE CELULAR_ACCIONANTE CIUDAD_ACCIONANTE NOMBRE_ACCIONADO NUM_RADICADO NUM_AUTO
do
  echo Ingrese la variable $variable
  read -r variable_value
  sed -i "s/$variable/$variable_value/g" "/usr/nuevo_officio.docx"
done

RETPATH=`pwd` 
cp plantilla_Auto.docx $1
FILE=$1       
rm -rf /var/tmp/docx    
mkdir /var/tmp/docx    
cp $FILE /var/tmp/docx
cd /var/tmp/docx    
mkdir tmp
unzip $FILE -d tmp
cd tmp/word
for variable in FECHA_OFFICIO NUMERO_OFFICIO NOMBRE_ACCIONANTE CORREO_ACCIONANTE CELULAR_ACCIONANTE CIUDAD_ACCIONANTE NOMBRE_ACCIONADO CORREO_ACCIONADO CIUDAD_ACCIONADO NUM_RADICADO NUM_AUTO 
do
  echo Ingrese la variable $variable
  read -r variable_value
  sed -i "s/$variable/$variable_value/g" document.xml
done
cd ..
zip -r ../${FILE} *
cp /var/tmp/docx/${FILE} ${RETPATH}
cd $RETPATH
rm -rf /var/tmp/docx 
