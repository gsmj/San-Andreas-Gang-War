from pysamp.textdraw import TextDraw


class TextDraws:
    logo = {}

    @classmethod
    def load(cls) -> None:
        cls.logo[0] = TextDraw.create(556.000000, 8.088897, "S")
        cls.logo[0].letter_size(0.449999, 1.600000)
        cls.logo[0].alignment(1)
        cls.logo[0].color(-16776961)
        cls.logo[0].set_shadow(0)
        cls.logo[0].set_outline(1)
        cls.logo[0].background_color(51)
        cls.logo[0].font(1)
        cls.logo[0].set_proportional(True)

        cls.logo[1] = TextDraw.create(565.000000, 8.088858, "AGW")
        cls.logo[1].letter_size(0.449999, 1.600000)
        cls.logo[1].alignment(1)
        cls.logo[1].color(-16776961)
        cls.logo[1].set_shadow(0)
        cls.logo[1].set_outline(1)
        cls.logo[1].background_color(51)
        cls.logo[1].font(1)
        cls.logo[1].set_proportional(True)

        cls.logo[2] = TextDraw.create(603.000000, 3.111082, "ld_chat:badchat")
        cls.logo[2].letter_size(0.000000, 0.000000)
        cls.logo[2].text_size(12.000000, 11.200004)
        cls.logo[2].alignment(1)
        cls.logo[2].color(-1)
        cls.logo[2].set_shadow(0)
        cls.logo[2].set_outline(0)
        cls.logo[2].font(4)
        return print(f"Created: TextDraw (server) -> ID: {[key for key in cls.logo]}")