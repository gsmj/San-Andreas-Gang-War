from pysamp.textlabel import create_3d_text_label

def create_labels() -> None:
    create_3d_text_label("Grove Street Families", 0x009900FF, 2514.3403, -1691.5911, 14.0460, 10, 0, test_line_of_sight=True)
    create_3d_text_label("The Ballas", 0xCC00FFFF, 2022.9318, -1120.2645, 26.4210+1, 10, 0, test_line_of_sight=True)
    create_3d_text_label("Los Santos Vagos", 0xffcd00FF, 2756.3645,-1182.8091, 69.4035+1, 10, 0, test_line_of_sight=True)
    create_3d_text_label("Varios Los Aztecas", 0x00B4E1FF, 2185.7717, -1815.2280, 13.5469, 10, 0, test_line_of_sight=True)
    create_3d_text_label("The Rifa", 0x6666FFFF, 2787.0764,-1926.1918, 13.5469+1, 10, 0, test_line_of_sight=True)