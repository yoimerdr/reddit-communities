from pyscript import Element

from py import ScreenSizes


def hide_element(element_id, hide_class="hide"):
    element = Element(element_id)
    element.add_class(hide_class)


def show_element(element_id, hide_class="hide"):
    element = Element(element_id)
    element.remove_class(hide_class)


def size_switch_option(option: str):
    if option == "S600P":
        return ScreenSizes.S600P
    elif option == "S720P":
        return ScreenSizes.S720P
    elif option == "S1080P":
        return ScreenSizes.S1080P
    elif option == "S1440P":
        return ScreenSizes.S1440P
    return ScreenSizes.S4K
