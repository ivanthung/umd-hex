import matplotlib.pyplot as plt

def create_project_shape_diagram(coords) -> plt.Figure:
    """Display the shape of the selected project"""
    x_coords = [point[0] for point in coords[0]]
    y_coords = [point[1] for point in coords[0]]

    # Close the polygon (Matplotlib expects the first and last points to be the same)
    x_coords.append(x_coords[0])
    y_coords.append(y_coords[0])

    # Create the plot
    fig, ax = plt.subplots(figsize=(1, 1))  # Set smaller figure size
    ax.plot(x_coords, y_coords, color="red")

    # Remove labels and axes
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_xticks([])  # Remove x ticks
    ax.set_yticks([])  # Remove y ticks
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Display in Streamlit
    return fig