import matplotlib.pyplot as plt
from matplotlib_venn import venn3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_venn_diagram(region_manager, master_frame):
    # Create a blank Venn diagram
    fig, ax = plt.subplots()
    venn = venn3(subsets=(1, 1, 1, 1, 1, 1, 1), set_labels=('A', 'B', 'C'))
    
    
    
    canvas = FigureCanvasTkAgg(fig, master=master_frame)
    canvas.draw()
    return canvas