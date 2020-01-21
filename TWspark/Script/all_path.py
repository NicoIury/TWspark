#script contenente tutti i path, includi i file negli script per averli sempre a disposizione
#per avere la compilazione autimatica consiglio
#from all_path import JSON_FILE, MODEL_PATH, INPUT_FOLDER, DATASET_FILE

i=0
if i==0:    #path di DARIO
    JSON_FILE = "/home/dario/Big_data_results/projectData/data.json"
    MODEL_PATH = "/home/dario/Scrivania/PoliBa/Big_data/sentiment140/modello"
    INPUT_FOLDER = "/home/dario/Scrivania/PoliBa/Big_data/sentiment140/"
    DATASET_FILE = "/home/dario/Big_data_results/projectData/dataset"
    GENERATED_DF = "/home/dario/Big_data_results/projectData/gen_df"
elif i==1:  #path di NICO
    DATASET_FILE = "/home/nico/Nico/pyProg/projData/dataset"
    MODEL_PATH = "/home/nico/Nico/pyProg/Big_data_2p/TWspark/model"
    INPUT_FOLDER = "/home/nico/Nico/pyProg/projData/"
    JSON_FILE = "/home/nico/Nico/pyProg/projData/data.json"
    GENERATED_DF = "/home/nico/Nico/pyProg/projData/gen_df"
