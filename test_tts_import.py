try:
    from piper import PiperVoice
    print("Import SUCCESS from 'piper'!")
except ImportError:
    try:
        from piper_voice import PiperVoice
        print("Import SUCCESS from 'piper_voice'!")
    except ImportError:
        print("Neither 'piper' nor 'piper_voice' worked.")
        import sys
        print("Python path:", sys.path)