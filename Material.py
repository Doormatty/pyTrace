from RGB import RGB


class Material:
    def __init__(self, color=RGB(25, 25, 25), opacity=1.0, reflect=0.0, luma=0.0):
        self.color = color
        self.opacity = opacity
        self.reflect = reflect
        self.luma = luma

    def __repr__(self):
        return f"Material(color={self.color}, opacity={self.opacity}, reflect={self.reflect}, luma={self.luma})"
