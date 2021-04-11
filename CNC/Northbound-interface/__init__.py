from pyspark import SparkContext, SparkConf
import time
sc = SparkContext(appName="word_counter")
for i in range(20):
    #lineas = sc.textFile("/quijote.txt", minPartitions=2)
    lineas = sc.textFile("/home/quijote.txt",minPartitions=2).flatMap(lambda line: line.split(" "))
    #lineas = sc.textFile("/home/words.txt")
    #Se extrae las palabras del texto y se cuentan

    # Para empezar a contar el tiempo

    start_time = time.time()
    print("---------------------------Time counter has started---------------------------")
    #contarPalabras = lineas.flatMap(lambda linea: linea.split(" ")).countByValue()
    contarPalabras = lineas.map(lambda word: (word, 1)).reduceByKey(lambda v1,v2:v1 +v2)
    #Se muestra las palabras con la cantidad de veces que tiene su aparición

    counted_list = contarPalabras.collect()
    #for palabra, contador in counted_list.items():
    #    print("{} : {}".format(palabra, contador))
    print(counted_list)
    file = open('record_3_machines.txt','a')
    execution_time = str(time.time()-start_time)
    file.write(execution_time +'\n')
    print(f"El programa tardo {(time.time()-start_time)} segundos en su ejecucion")
