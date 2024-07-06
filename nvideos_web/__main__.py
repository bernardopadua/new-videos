from nvideos_web.factory import createApp

if __name__ == "__main__":
    createApp().run("0.0.0.0", 8080, True, False, use_reloader=False)