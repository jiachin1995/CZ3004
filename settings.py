comms = False                               #print communication logs
logging = False                             #print logs statements, normally for debugging purposes
mapformat_returntype_isHex = True           #default true. If false, returns map format as bits instead of hex
optimise_diagonals = False                  #If True, optimise shortest path such that robot will make diagonal movements

front_sensors_range = 2                     #biggest integer that sensors will return to algo
left_sensors_range = 2
right_sensors_range = 5

right_sensors_position = 1                  #position of right sensor, front, mid or back

"""2 may not be debugged. Use after confirming that it works."""
findallimages = 1                           #whether to find all images. 0 = no images, 1 = some images, 2 = all images
images_threshold = 5                        #if findallimages>0, how many images to find before stopping image finding
save_images = False                         #save image for every identification

imageslabels = [                            #images labels
        '1',        #white up arrow
        '2',        #red down arrow
        '3',        #green right arrow
        '4',        #blue left arrow
        
        '5',        #yellow zero
        '6',        #blue one
        '7',        #green two
        '8',        #red three
        '9',        #white four
        '10',       #yellow five
        
        '11',       #red A
        '12',       #green B
        '13',       #white C
        '14',       #blue D
        '15',       #yellow E
        
        'default',  #no images found
    ]
       



giveupspelunk = False                       #whether to give up on spelunk cause hardware cmi
skipwhiteimages = True                      #whether to give up on white images cause image rec cmi

"""
    considering
    logging = {
        "verbose",  #all logs
        "debug",    #include impt function outputs
        "impt",     #select few logs
        None,
    }
"""
