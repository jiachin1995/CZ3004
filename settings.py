
comms = True                                #print communication logs
logging = False                             #print logs statements, normally for debugging purposes
mapformat_returntype_isHex = True           #default true. If false, returns map format as bits instead of hex
optimise_diagonals = False                  #If True, optimise shortest path such that robot will make diagonal movements

front_sensors_range = 3                     #biggest integer that sensors will return to algo
left_sensors_range = 3

"""2 may not be implemented. ask me before changing to this setting."""
findallimages = 1                           #whether to find all images. 0 = no images, 1 = some images, 2 = all images
images_threshold = 5                        #if findallimages>0, how many images to find before stopping image finding
save_images = False                         #save image for every identification


"""
    considering
    logging = {
        "verbose",  #all logs
        "debug",    #include impt function outputs
        "impt",     #select few logs
        None,
    }
"""