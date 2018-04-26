try:
    from .run import launch
except (ImportError, SystemError):
    from smartvadhis2.run import launch

if __name__ == '__main__':
    launch()
