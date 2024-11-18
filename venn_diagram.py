import matplotlib.pyplot as plt
from matplotlib_venn import venn3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from region_struct import Status

def create_venn_diagram(region_manager, master_frame):
    # Create a Venn diagram
    fig, ax = plt.subplots()
    venn = venn3(subsets=(1, 1, 1, 1, 1, 1, 1, 1), set_labels=('A', 'B', 'C'))
    
    # Set up defualt diagram
    for subset in ('100', '010', '001', '110', '101', '011', '111'):
        venn.get_patch_by_id(subset).set_facecolor('white')
        venn.get_patch_by_id(subset).set_edgecolor('black')
        venn.get_label_by_id(subset).set_text('')
    
    
    for region_tuple, region in region_manager.regions.items():    
        print(region_tuple)
        subset_label = ''.join(['1' if x else '0' for x in region_tuple])
        print(subset_label)
        
        if region.status == Status.CONTAINS:
            venn.get_label_by_id(subset_label).set_text('O')
        elif region.status == Status.UNINHABITABLE:
            venn.get_label_by_id(subset_label).set_text('X')
            venn.get_patch_by_id(subset_label).set_facecolor('grey')
            venn.get_patch_by_id(subset_label).set_alpha(0.5)
        
    
    
    canvas = FigureCanvasTkAgg(fig, master=master_frame)
    canvas.draw()
    return canvas

