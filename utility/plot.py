import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
import skimage.color as color
import numpy as np
import os

from sklearn.metrics import recall_score, precision_score, accuracy_score



# Retrieve the Pokemon along with its type, name, and the number of what occurence.  
# pkns_names is an array of pokemonName occurence  
def plot_chain(type, pkmns_names):
    main_folder = "./Pokemon/dataset/"
    img_folder = os.path.join(main_folder,type)
    n = len(pkmns_names)
    plt.figure(figsize=(8,24))
    for idx, pkm in enumerate(pkmns_names):
        file = "{name}.png".format(name=pkm)
        img = mpimg.imread(os.path.join(img_folder,file))
        plt.subplot(1,n,idx+1) # a single row, n column, the position of the current subplot
        plt.imshow(img)
    plt.show()   

def plot_sprite(name, type_1, type_2, color_1, color_2, pred=None, save=None, save_path="./classification"):
    # print(name)
    # Defining the dimensions of the grid
    if pred:
        grid_rows = 2
        grid_cols = 2
        figsize = (8, 4.4)
        width_ratios = (1, 1)
        sprite_grid = 0
        pred_grid = 1
        type_grid = 2
    else:
        grid_rows = 2
        grid_cols = 1
        figsize = (4, 4.4)
        width_ratios = (1,)
        sprite_grid = 0
        type_grid = 1

    # Create the figure and grid specification
    fig = plt.figure(figsize=figsize)
    gs = gridspec.GridSpec(grid_rows, grid_cols, height_ratios=(10, 1), width_ratios=width_ratios)

    # Find the first Pokémon image
    main_folder = "./Pokemon/dataset/"
    img_folder = os.path.join(main_folder, type_1)
    file = "{name}_1.png".format(name=name)
    img = mpimg.imread(os.path.join(img_folder, file))

    # Plot the sprite of the Pokémon
    ax_sprite = plt.subplot(gs[sprite_grid])
    ax_sprite.imshow(img)

    # Plot the true type of the Pokemon
    ax_type = plt.subplot(gs[type_grid])
    plt.axis("off")

    # Create a rectangle for the first type
    type_box_01 = patches.Rectangle(
        (0, 0),
        0.5 if type_2 else 1,
        1,
        fc=color_1,
        ec="#FFFFFF"
    )
    ax_type.add_patch(type_box_01)
    # Annotate the label for the first type
    ax_type.annotate(type_1, (0.25 if type_2 else 0.5, 0.5), color='w', weight='bold',
                     fontsize=12, ha='center', va='center')
                     

    # If there is a second type, create a rectangle for it
    if type_2:
        type_box_02 = patches.Rectangle(
            (0.5, 0),
            0.5,
            1,
            fc=color_2,
            ec="#FFFFFF"
        )
        ax_type.add_patch(type_box_02)
        # Annotate the label for the second type
        ax_type.annotate(type_2, (0.75, 0.5), color='w', weight='bold',
                         fontsize=12, ha='center', va='center')

    # Plot the predictions
    if pred:
        ax_pred = plt.subplot(gs[pred_grid])
        plt.axis("off")

        # Sort the predictions by probability in descending order
        pred_list = list(pred.items())
        pred_list = sorted(pred_list, key=lambda x: x[1], reverse=True)
        for idx, (pred_type, pred_prob) in enumerate(pred_list):
            # Create a rectangle for each predicted type
            pred_box = patches.Rectangle(
                (0, 0.8 - 0.2 * idx),
                0.5,
                0.2,
                fc=color_1,
                ec="#FFFFFF"
            )
            ax_pred.add_patch(pred_box)
            # Annotate the label for each predicted type
            ax_pred.annotate(type_1, (0.25, 0.9 - 0.2 * idx), color='#FFFFFF', weight='bold',
                             fontsize=12, ha='center', va='center')
            # Annotate the probability for each predicted type
            ax_pred.annotate("{:.0%}".format(pred_prob), (0.75, 0.9 - 0.2 * idx), color='#000000', weight='bold',
                             fontsize=16, ha='center', va='center')

    # Save the figure if specified
    if save:
        correct_path = os.path.join(save_path, "correct")
        wrong_path = os.path.join(save_path, "wrong")
        if not os.path.exists(correct_path):
            os.makedirs(correct_path)
        if not os.path.exists(wrong_path):
            os.makedirs(wrong_path)
        if type_1 == pred_list[0][0]:
            save_file = os.path.join(correct_path, save)
        else:
            save_file = os.path.join(wrong_path, save)
        fig.savefig(save_file)

    plt.show()   
                                  

def plot_display(rec):
    plot_sprite(
        name = rec["name"],
        type_1 = rec["type_01"],
        type_2 = rec["type_02"],
        color_1 = rec["text_color_type_01"],
        color_2 = rec["text_color_type_02"]
    )    
    
# def plot_evaluation(label,y_true,y_pred,type_dict=load_type_dict()):
#     y_pred = np.argmax(y_pred,axis=1)+1
#     y_true = np.argmax(y_true,axis=1)+1    
#     #Evaluate model metrics over input data
#     recall = recall_score(y_true, y_pred, average=None)
#     precision = precision_score(y_true, y_pred, average=None)
#     accuracy = accuracy_score(y_true, y_pred)
    
#     #Create grid for plotting
#     fig = plt.figure(figsize=(8.8,5))
#     gs = gridspec.GridSpec(2,1, height_ratios = (1,9))
       
#     #Plotting model-level metrics
#     ax = plt.subplot(gs[0])     
#     ax.axis("off")    
#     ax.annotate("{} Accuracy = {:.0%}".format(label,accuracy), (0.5, 0.5), color='#000000', 
#                 fontsize=18, ha='center', va='center')     
        
#     #Ploting class-level metrics
#     ax = plt.subplot(gs[1]) 
#     ax.axis("off")    
    
#     #In some cases, there are no records of some classes (usually 3:Flying) Here, we fill
#     #up the missing classes with 'None' values.
#     unique_labels = np.unique(np.vstack([y_true,y_pred]))
#     metrics = dict( (key, {"recall" : None, "precision" : None}) for key in range(1,19))
#     for key, v_recall, v_precision in zip(unique_labels, recall, precision):
#         metrics[key]["recall"] = v_recall
#         metrics[key]["precision"] = v_precision

#     #Writing the headers of the class table
#     ax.annotate("Precision", (0.27, 19/20), color='#000000', weight='bold', 
#                 fontsize=12, ha='center', va='center')     
#     ax.annotate("Recall", (0.4, 19/20), color='#000000', weight='bold', 
#                 fontsize=12, ha='center', va='center')        
#     ax.annotate("Precision", (0.77, 19/20), color='#000000', weight='bold', 
#                 fontsize=12, ha='center', va='center')        
#     ax.annotate("Recall", (0.9, 19/20), color='#000000', weight='bold', 
#                 fontsize=12, ha='center', va='center')            
    
#     #Writing the metrics for each class
#     for i, (pkm_type, metric) in enumerate(metrics.items()):
#         column = int(i/9)
#         row = i % 9 + 1
#         left = column*0.5
#         top = 1.0-(row+1)*1/10
#         type_box = patches.Rectangle(
#             (left,top),
#             0.2,
#             1/9,
#             fc = type_dict[pkm_type]["color"],
#             ec = "#FFFFFF"            
#         ) 
#         ax.add_patch(type_box)
#         ax.annotate(type_dict[pkm_type]["label"], (left+0.1, top+1/20), color='#FFFFFF', weight='bold', 
#                     fontsize=12, ha='center', va='center')  
#         #Precision
#         if metric["precision"] is not None:
#             ax.annotate("{:.0%}".format(metric["precision"]), (left+0.27, top+1/20), color='#000000', 
#                         fontsize=14, ha='center', va='center')    
#         #Recall
#         if metric["recall"] is not None:
#             ax.annotate("{:.0%}".format(metric["recall"]), (left+0.40, top+1/20), color='#000000', 
#                         fontsize=14, ha='center', va='center')          