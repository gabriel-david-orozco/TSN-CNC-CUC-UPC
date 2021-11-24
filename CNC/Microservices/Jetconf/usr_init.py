from colorlog import info


def jc_startup():
    info("Backend: init")


def jc_end():
    info("Backend: cleaning up")
