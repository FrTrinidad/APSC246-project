import pygame

class SoungManager:
# Manages all the game audio (sound effects, music, etc)
# Handles the loading, playing, and volume control

# As it is now there are no audio files, so it uses placeholder/silent sounds.

    def __init__(self):
        # Initialize pygame mixer if its not already
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        # Volume level (0.0 to 1.0, sets initial volume)
        self.volume_level = 0.5
        
        # Sound effect collection
        # Empty for now
        self.sounds = {}
        
        # Track if audio is available
        self.audio_available = pygame.mixer.get_init() is not None
        
        # Load all game sounds
        self._load_sounds()
    
    def _load_sounds(self):
        # Load all audio files used in the game
        # Define sound file paths, this is placeholder stuff, these dont actually exist as of now
        sound_files = {
            "paddle_hit": "sounds/paddle_hit.wav",
            "wall_hit": "sounds/wall_hit.wav",
            "score": "sounds/score.wav",
            "menu_move": "sounds/menu_move.wav",
            "menu_select": "sounds/menu_select.wav",
            "game_start": "sounds/game_start.wav",
            "game_win": "sounds/game_win.wav",
        }
        
        for name, path in sound_files.items():
            self._load_sound(name, path)

    def _load_sound(self, name, filepath):
        # Load a single sound file. 
        # Creates a placeholder if file not found.
        # name is the key to store the sound under
        # filepath is the path to the audio file
        
        
        try:
            # Tries to load the sound file from the path given
            sound = pygame.mixer.Sound(filepath)

            # Sets the sound volume baed on the current volume level
            sound.set_volume(self.volume_level)

            # Stores the loaded sound in a dictionary for further use
            # Uses the name as the key
            self.sounds[name] = sound

        # In case the fie isnt found
        except (FileNotFoundError, pygame.error):
            # Sound file not found
            # Create placeholder entry
            self.sounds[name] = None
    
        #YK WHAT ill do this later of delegate, this isnt even my job