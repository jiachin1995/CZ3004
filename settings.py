
comms = True                                #print communication logs
logging = False                             #print logs statements, normally for debugging purposes
mapformat_returntype_isHex = True           #default true. If false, returns map format as bits instead of hex
optimise_diagonals = False                  #If True, optimise shortest path such that robot will make diagonal movements

front_sensors_range = 3                     #biggest integer that sensors will return to algo
left_sensors_range = 3
right_sensors_range = 5

right_sensors_position = 0                  #position of right sensor, front, mid or back

"""2 may not be debugged. Use after confirming that it works."""
findallimages = 0                           #whether to find all images. 0 = no images, 1 = some images, 2 = all images
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
