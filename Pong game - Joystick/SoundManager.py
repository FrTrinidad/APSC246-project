import pygame

class SoundManager:
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
        
        # Load all game sounds & music
        self.load_sounds()
        self.load_music()
    
    def load_music(self):
        try:
            pygame.mixer.music.load("audio/music.mp3")
            pygame.mixer.music.set_volume(self.volume_level * 0.5)  # So that the music quieter than SFX
        except (FileNotFoundError, pygame.error):
            pass

    def play_music(self):
        try:
            pygame.mixer.music.play(-1)  # -1 = loop forever
        except:
            pass

    def stop_music(self):
        pygame.mixer.music.stop()

    def load_sounds(self):
        # Load all audio files used in the game
        # Maps the sound names to their files
        sound_files = {
            "paddle_hit": "audio/hit.wav",
            "wall_hit": "audio/hit.wav",
            "score": "audio/point.wav",
            "menu_move": "audio/updown.wav",
            "menu_select": "audio/enter.wav",
            "countdown": "audio/countdown.mp3",
            "win": "audio/win.mp3",
            "lose": "audio/lose.mp3"
        }

        for name, path in sound_files.items():
            self.load_sound(name, path)

    def load_sound(self, name, filepath):
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
        # This shouldnt happen, but this is a checked exception soo
        except (FileNotFoundError, pygame.error):
            # Sound file not found
            # Create placeholder entry
            self.sounds[name] = None
    
    def play(self, sound_name):
        # Plays a sound by name        
        sound = self.sounds.get(sound_name)

        if sound:
            sound.play()

    def play_paddle_hit(self):
        self.play("paddle_hit")
    
    def play_wall_hit(self):
        self.play("wall_hit")
    
    def play_score(self):
        self.play("score")
    
    def play_menu_move(self):
        self.play("menu_move")
    
    def play_menu_select(self):
        self.play("menu_select")
    
    def play_countdown(self):
        self.play("countdown")
    
    def play_win(self):
        self.play("win")

    def play_lose(self):
        self.play("lose")

    def set_volume(self, level):
        # level is 0-100 
        # We convert it to 0.0-1.0
        self.volume_level = level / 100.0

        for sound in self.sounds.values():
            if sound:
                sound.set_volume(self.volume_level)

        # Updates the music volume as well
        pygame.mixer.music.set_volume(self.volume_level * 0.5)
